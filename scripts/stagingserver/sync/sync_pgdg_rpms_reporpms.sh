#!/usr/bin/bash

set -euo pipefail

had_errors=0

# Source central configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_FILE="${SCRIPT_DIR}/sync_pgdg_rpms_config.sh"

if [[ ! -f "$CONFIG_FILE" ]]; then
	echo "ERROR: Configuration file not found: $CONFIG_FILE" >&2
	exit 1
fi

source "$CONFIG_FILE"

# Runtime variables
OS=""
VER=""
ARCH=""
DRY_RUN=false
DEBUG=false

# Help
usage() {
	cat <<EOF
Usage: $0 [options]

Finds the latest pgdg-redhat-repo / pgdg-fedora-repo / pgdg-amazonlinux-repo
RPM under each common/<os>/<osname>-<ver>-<arch> directory and republishes it
under reporpms/EL-<ver>-<arch> (redhat), reporpms/F-<ver>-<arch> (fedora), or
reporpms/AL-<ver>-<arch> (amzn), removing the previous repo RPM and
re-pointing the "*-repo-latest.noarch.rpm" symlink at the new one.

Optional:
  --os           Restrict to one OS: redhat, fedora, amzn (default: all three)
  --ver          Restrict to one OS version (must be valid for --os)
  --arch         Restrict to one architecture (must be valid for --os)
  --dry-run      Show what would change without touching any files
  --debug        Show detailed debug output

Examples:
  $0
  $0 --os redhat --ver 10.2 --arch x86_64
  $0 --os fedora --dry-run

EOF
	exit "${1:-1}"
}

# Contains helper
contains() {
	local val="$1"
	shift
	for item in "$@"; do [[ "$item" == "$val" ]] && return 0; done
	return 1
}

# Parse arguments
while [[ $# -gt 0 ]]; do
	case "$1" in
	--help|-h)
		usage 0
		;;
	--os)
		OS="$2"
		shift 2
		;;
	--ver)
		VER="$2"
		shift 2
		;;
	--arch)
		ARCH="$2"
		shift 2
		;;
	--dry-run)
		DRY_RUN=true
		shift
		;;
	--debug)
		DEBUG=true
		shift
		;;
	*)
		echo "Unknown option: $1"
		usage
		;;
	esac
done

if [[ -n "$OS" ]] && ! contains "$OS" "redhat" "fedora" "amzn"; then
	echo "Invalid OS: $OS (must be redhat, fedora, or amzn)"
	usage
fi

# Update one <os>/<ver>/<arch> combination.
# Copies the newest repo RPM from src_dir into dest_dir, re-links
# "*-repo-latest.noarch.rpm" at it, and sweeps dest_dir clean of every other
# file/symlink starting with $reponame (old versioned RPMs, stray or
# oddly-named symlinks left over from before this script existed, etc.).
update_repo_rpm() {
	local os="$1"
	local ver="$2"
	local arch="$3"
	local reponame="$4"
	local src_dir="$5"
	local dest_dir="$6"

	if [[ ! -d "$src_dir" ]]; then
		$DEBUG && echo "  [DEBUG] Source dir missing, skipping: $src_dir"
		return 0
	fi

	if [[ ! -d "$dest_dir" ]]; then
		echo "  [WARN] Destination dir missing, skipping: $dest_dir" >&2
		had_errors=1
		return 0
	fi

	local latest
	latest="$(find "$src_dir" -maxdepth 1 -type f -name "${reponame}-*.rpm" -printf '%f\n' | sort -V | tail -n1)"

	if [[ -z "$latest" ]]; then
		echo "  [WARN] No ${reponame} RPM found in $src_dir" >&2
		had_errors=1
		return 0
	fi

	local symlink_name="${reponame}-latest.noarch.rpm"

	local need_copy=false
	[[ -f "$dest_dir/$latest" ]] || need_copy=true

	local current_target=""
	if [[ -L "$dest_dir/$symlink_name" ]]; then
		current_target="$(readlink "$dest_dir/$symlink_name")"
	fi

	# Anything under dest_dir named "$reponame-*" other than the current
	# latest RPM and the correctly-named symlink is cruft to remove.
	local -a cruft=()
	local entry base
	while IFS= read -r -d '' entry; do
		base="$(basename "$entry")"
		[[ "$base" == "$latest" ]] && continue
		[[ "$base" == "$symlink_name" ]] && continue
		cruft+=("$entry")
	done < <(find "$dest_dir" -maxdepth 1 \( -type f -o -type l \) -name "${reponame}-*" -print0)

	if ! $need_copy && [[ "$current_target" == "$latest" ]] && [[ ${#cruft[@]} -eq 0 ]]; then
		$DEBUG && echo "  [DEBUG] $os $ver $arch already up to date ($latest)"
		return 0
	fi

	echo "  Updating $os $ver ($arch): ${current_target:-<none>} -> $latest"

	if $DRY_RUN; then
		$need_copy && echo "  [DRY-RUN] cp $src_dir/$latest $dest_dir/$latest"
		[[ "$current_target" != "$latest" ]] && echo "  [DRY-RUN] ln -sfn $latest $dest_dir/$symlink_name"
		for entry in "${cruft[@]}"; do
			echo "  [DRY-RUN] rm -f $entry"
		done
		return 0
	fi

	if $need_copy && ! cp -f "$src_dir/$latest" "$dest_dir/$latest"; then
		echo "  [ERROR] Failed to copy $latest into $dest_dir" >&2
		had_errors=1
		return 0
	fi

	if [[ "$current_target" != "$latest" ]]; then
		[[ -L "$dest_dir/$symlink_name" ]] && unlink "$dest_dir/$symlink_name"
		ln -s "$latest" "$dest_dir/$symlink_name"
	fi

	for entry in "${cruft[@]}"; do
		rm -f "$entry"
	done
}

process_os() {
	local os="$1"
	local osname="$2"
	local reponame="$3"
	local destprefix="$4"

	local tmp_var="BASE_DIR_${os}"
	local base_dir="${!tmp_var}"

	local -n ver_ref="VALID_VER_${os}"
	local -a ver_list=("${ver_ref[@]}")

	if [[ -n "$VER" ]]; then
		if ! contains "$VER" "${ver_list[@]}"; then
			$DEBUG && echo "[DEBUG] Version $VER not valid for $os, skipping $os"
			return 0
		fi
		ver_list=("$VER")
	fi

	echo ""
	echo "================================================"
	echo "Processing $os repo RPMs"
	echo "================================================"

	for ver in "${ver_list[@]}"; do
		# Not every version supports every arch in VALID_ARCH_<os> — see
		# VALID_ARCH_OVERRIDES in sync_pgdg_rpms_config.sh
		local -a ver_valid_arch
		get_valid_arch_for "$os" "$ver" ver_valid_arch

		local -a arch_list=("${ver_valid_arch[@]}")
		if [[ -n "$ARCH" ]]; then
			if ! contains "$ARCH" "${ver_valid_arch[@]}"; then
				$DEBUG && echo "[DEBUG] Arch $ARCH not valid for $os $ver, skipping $os $ver"
				continue
			fi
			arch_list=("$ARCH")
		fi

		for arch in "${arch_list[@]}"; do
			local src_dir="${base_dir}/common/${os}/${osname}-${ver}-${arch}"
			local dest_dir="${base_dir}/reporpms/${destprefix}-${ver}-${arch}"
			update_repo_rpm "$os" "$ver" "$arch" "$reponame" "$src_dir" "$dest_dir"
		done
	done
}

if [[ -z "$OS" || "$OS" == "redhat" ]]; then
	process_os "redhat" "rhel" "pgdg-redhat-repo" "EL"
fi

if [[ -z "$OS" || "$OS" == "fedora" ]]; then
	process_os "fedora" "fedora" "pgdg-fedora-repo" "F"
fi

if [[ -z "$OS" || "$OS" == "amzn" ]]; then
	process_os "amzn" "amzn" "pgdg-amazonlinux-repo" "AL"
fi

echo ""
if [[ "$had_errors" -eq 1 ]]; then
	echo "[WARN] One or more repo RPM updates failed." >&2
	exit 1
else
	echo "All repo RPM symlinks up to date."
	exit 0
fi
