# Bash completion for sync_pgdg_rpms.sh

# Source central configuration
_sync_pgdg_rpms_get_config() {
	local script_path config_file

	# Try to find the config file
	# First, look in the same directory as the script being completed
	for arg in "${COMP_WORDS[@]}"; do
		if [[ -f "$arg" ]]; then
			script_path="$(cd "$(dirname "$arg")" && pwd)"
			config_file="${script_path}/sync_pgdg_rpms_config.sh"
			break
		fi
	done

	# If not found, try common locations
	if [[ ! -f "$config_file" ]]; then
		for dir in ~/bin /usr/local/bin "$PWD"; do
			if [[ -f "${dir}/sync_pgdg_rpms_config.sh" ]]; then
				config_file="${dir}/sync_pgdg_rpms_config.sh"
				break
			fi
		done
	fi

	if [[ -f "$config_file" ]]; then
		source "$config_file"
		return 0
	else
		# Fallback to hardcoded values if config not found
		return 1
	fi
}

_sync_pgdg_rpms() {
	local cur prev opts os_choice sync_mode
	local i v

	COMPREPLY=()
	cur="${COMP_WORDS[COMP_CWORD]}"
	prev="${COMP_WORDS[COMP_CWORD - 1]}"

	opts="--os --arch --ver --sync --dry-run --debug"

	# Try to load config, use fallback if not available
	if ! _sync_pgdg_rpms_get_config; then
		# Fallback values
		VALID_OS=("redhat" "fedora" "sles" "opensuse" "amzn")
		VALID_ARCH_redhat=("aarch64" "ppc64le" "x86_64")
		VALID_ARCH_fedora=("x86_64")
		VALID_ARCH_sles=("x86_64")
		VALID_ARCH_opensuse=("x86_64")
		VALID_ARCH_amzn=("x86_64" "aarch64")
		VALID_VER_redhat=("10.2" "10.1" "10.0" "9.8" "9.7" "9.6" "8.10")
		VALID_VER_fedora=("44" "43")
		VALID_VER_sles=("15.6" "15.7" "16.0")
		VALID_VER_opensuse=("16.0")
		VALID_VER_amzn=("2023")
		PG_ALL_VERSIONS=(18 17 16 15 14)
		PG_TEST_VERSIONS=(20 19 18 17 16 15 14)
	fi

	# PG versions that only exist in testing (not yet in PG_ALL_VERSIONS),
	# so --sync completion doesn't offer the same version number twice
	local -a pg_testing_only=()
	local pgver already
	for pgver in "${PG_TEST_VERSIONS[@]}"; do
		already=0
		for v in "${PG_ALL_VERSIONS[@]}"; do
			[[ "$v" == "$pgver" ]] && already=1 && break
		done
		[[ "$already" -eq 0 ]] && pg_testing_only+=("$pgver")
	done

	# Extract --os value if provided
	for i in "${!COMP_WORDS[@]}"; do
		if [[ "${COMP_WORDS[i]}" == "--os" && -n "${COMP_WORDS[i + 1]}" ]]; then
			os_choice="${COMP_WORDS[i + 1]}"
		fi
		if [[ "${COMP_WORDS[i]}" == "--sync" ]]; then
			sync_mode=1
		fi
	done

	case "$prev" in
	--os)
		COMPREPLY=($(compgen -W "${VALID_OS[*]}" -- "$cur"))
		return 0
		;;
	--arch)
		# Provide architecture options based on OS if known
		if [[ "$os_choice" == "redhat" ]]; then
			COMPREPLY=($(compgen -W "${VALID_ARCH_redhat[*]}" -- "$cur"))
		elif [[ "$os_choice" == "fedora" ]]; then
			COMPREPLY=($(compgen -W "${VALID_ARCH_fedora[*]}" -- "$cur"))
		elif [[ "$os_choice" == "sles" ]]; then
			COMPREPLY=($(compgen -W "${VALID_ARCH_sles[*]}" -- "$cur"))
		elif [[ "$os_choice" == "opensuse" ]]; then
			COMPREPLY=($(compgen -W "${VALID_ARCH_opensuse[*]}" -- "$cur"))
		elif [[ "$os_choice" == "amzn" ]]; then
			COMPREPLY=($(compgen -W "${VALID_ARCH_amzn[*]}" -- "$cur"))
		else
			# If OS not specified yet, show all possible architectures
			COMPREPLY=($(compgen -W "aarch64 ppc64le x86_64" -- "$cur"))
		fi
		return 0
		;;
	--ver)
		if [[ "$os_choice" == "redhat" ]]; then
			COMPREPLY=($(compgen -W "${VALID_VER_redhat[*]}" -- "$cur"))
		elif [[ "$os_choice" == "fedora" ]]; then
			COMPREPLY=($(compgen -W "${VALID_VER_fedora[*]}" -- "$cur"))
		elif [[ "$os_choice" == "sles" ]]; then
			COMPREPLY=($(compgen -W "${VALID_VER_sles[*]}" -- "$cur"))
		elif [[ "$os_choice" == "opensuse" ]]; then
			COMPREPLY=($(compgen -W "${VALID_VER_opensuse[*]}" -- "$cur"))
		elif [[ "$os_choice" == "amzn" ]]; then
			COMPREPLY=($(compgen -W "${VALID_VER_amzn[*]}" -- "$cur"))
		else
			# If OS not specified, show all versions
			local all_versions="${VALID_VER_redhat[*]} ${VALID_VER_fedora[*]} ${VALID_VER_sles[*]} ${VALID_VER_opensuse[*]} ${VALID_VER_amzn[*]}"
			COMPREPLY=($(compgen -W "$all_versions" -- "$cur"))
		fi
		return 0
		;;
	--sync)
		# Offer sync options: common, extras, testing, non-free, pg, or PG versions
		# (stable + testing-only, e.g. 19/20 - only meaningful combined with testing)
		COMPREPLY=($(compgen -W "common extras testing non-free pg ${PG_ALL_VERSIONS[*]} ${pg_testing_only[*]}" -- "$cur"))
		return 0
		;;
	*)
		# If we're in --sync mode (following --sync values), continue offering sync options
		if [[ -n "$sync_mode" && "$cur" != --* ]]; then
			COMPREPLY=($(compgen -W "common extras testing non-free pg ${PG_ALL_VERSIONS[*]} ${pg_testing_only[*]}" -- "$cur"))
			return 0
		fi
		;;
	esac

	# Default: offer main options
	if [[ "$cur" == --* ]]; then
		COMPREPLY=($(compgen -W "$opts" -- "$cur"))
	fi
}

# Register the function for your script name
complete -F _sync_pgdg_rpms sync_pgdg_rpms.sh
