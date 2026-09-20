#!/usr/bin/bash

#########################################################
#							#
# Devrim Gündüz <devrim@gunduz.org> - 2026		#
#							#
# Daily Alpha Build Script for PostgreSQL		#
#							#
#########################################################

set -e  # Exit on error
set -u  # Exit on undefined variable

# Include common values:
source ~/bin/global.sh

# Script configuration
readonly SCRIPT_NAME=$(basename "$0")
readonly BUILD_TYPE="alpha"
readonly RPM_BASE_DIR="${HOME}/rpm${pgAlphaVersion}testing"
readonly GIT_REPO_DIR="${HOME}/git/pgrpms/rpm/redhat/main/non-common/postgresql-${pgAlphaVersion}/${git_os}"

#########################################################
# Functions
#########################################################

# Display usage information
usage() {
	cat << EOF
Usage: $SCRIPT_NAME [OPTIONS]

Build daily PostgreSQL ${pgAlphaVersion} alpha packages.

Options:
  -h, --help           Show this help message
  -v, --verbose        Enable verbose output
  --skip-cleanup       Skip cleaning old packages
  --skip-sync          Skip package sync at the end

Description:
  This script performs the following operations:
  1. Prepares the build environment
  2. Builds PostgreSQL ${pgAlphaVersion} testing packages
  3. Cleans old packages (>1 day)
  4. Signs all RPM packages
  5. Syncs packages to repositories

Examples:
  $SCRIPT_NAME                 # Normal build
  $SCRIPT_NAME --verbose       # Build with verbose output
  $SCRIPT_NAME --skip-sync     # Build without syncing

EOF
	exit 0
}

# Log message with timestamp
log() {
	local level="$1"
	shift
	local message="$*"
	local timestamp=$(date '+%Y-%m-%d %H:%M:%S')

	case "$level" in
		INFO)
			echo "${green}[${timestamp}] [INFO]${reset} ${message}"
			;;
		WARN)
			echo "${blue}[${timestamp}] [WARN]${reset} ${message}"
			;;
		ERROR)
			echo "${red}[${timestamp}] [ERROR]${reset} ${message}" >&2
			;;
		SUCCESS)
			echo "${green}[${timestamp}] [SUCCESS]${reset} ${message}"
			;;
		*)
			echo "[${timestamp}] ${message}"
			;;
	esac
}

# Error handler
error_exit() {
	log ERROR "$1"
	exit 1
}

# Check if required directories exist
check_prerequisites() {
	log INFO "Checking prerequisites..."

	if [ ! -d "$GIT_REPO_DIR" ]; then
		error_exit "Git repository directory not found: $GIT_REPO_DIR"
	fi

	if [ ! -f ~/bin/packagesync.sh ]; then
		error_exit "Package sync script not found: ~/bin/packagesync.sh"
	fi

	# Check if GPG agent is running
	if ! pgrep -x gpg-agent > /dev/null; then
		error_exit "GPG agent is not running. Start it with: gpg-agent --daemon"
	fi

	log SUCCESS "Prerequisites check passed"
}

# Clean and prepare build environment
prepare_build_environment() {
	log INFO "Preparing build environment..."

	cd "$GIT_REPO_DIR" || error_exit "Failed to change to directory: $GIT_REPO_DIR"

	log INFO "Cleaning git repository..."
	git clean -dfx || error_exit "Git clean failed"

	log SUCCESS "Build environment prepared"
}

# Prepare PostgreSQL source
prepare_postgresql_source() {
	log INFO "Preparing PostgreSQL ${pgAlphaVersion} source..."

	cd "$GIT_REPO_DIR" || error_exit "Failed to change to directory: $GIT_REPO_DIR"

	make prep${pgAlphaVersion} || error_exit "Source preparation failed"

	log SUCCESS "PostgreSQL source prepared"
}

# Build PostgreSQL packages
build_postgresql_packages() {
	log INFO "Building PostgreSQL ${pgAlphaVersion} testing packages..."

	cd "$GIT_REPO_DIR" || error_exit "Failed to change to directory: $GIT_REPO_DIR"

	if make noprepbuild${pgAlphaVersion}testing; then
		log SUCCESS "PostgreSQL packages built successfully"
		return 0
	else
		error_exit "Package build failed"
	fi
}

# Clean old packages
clean_old_packages() {
	if [ "$SKIP_CLEANUP" = true ]; then
		log WARN "Skipping old package cleanup (--skip-cleanup specified)"
		return 0
	fi

	log INFO "Cleaning old packages (>1 day old)..."

	local deleted_count=0
	local old_files

	# Delete old files (>1 day old). A here-string, not process substitution, as
	# the scripts also run under "sh" (POSIX mode), where process substitution
	# does not exist in bash 4.4:
	old_files=$(find "${RPM_BASE_DIR}"* -maxdepth 3 -mtime +1 -type f 2>/dev/null || true)
	while IFS= read -r file; do
		if [ -f "$file" ]; then
			rm -f "$file"
			deleted_count=$((deleted_count + 1))
			[ "$VERBOSE" = true ] && log INFO "Deleted: $file"
		fi
	done <<< "$old_files"

	log INFO "Deleted $deleted_count old file(s)"

	# Remove signature files
	log INFO "Removing old signature files..."
	local sig_count=0
	local sig_files

	sig_files=$(find "${RPM_BASE_DIR}"* -iname "*.sig" 2>/dev/null || true)
	while IFS= read -r sig_file; do
		if [ -f "$sig_file" ]; then
			rm -vf "$sig_file"
			sig_count=$((sig_count + 1))
		fi
	done <<< "$sig_files"

	log INFO "Removed $sig_count signature file(s)"
	log SUCCESS "Old package cleanup completed"
}

# Sign RPM packages
sign_rpm_packages() {
	log INFO "Signing RPM packages..."

	# Extract the directory name from RPM_BASE_DIR (e.g., "rpm19testing")
	local rpm_location=$(basename "${RPM_BASE_DIR}")

	# Set variables for sign_package function
	# Use wildcards to sign all packages (not filtering by name/version)
	export signPackageName=""
	export packageVersion=""

	if sign_package "$rpm_location"; then
		log SUCCESS "Package signing completed"
	else
		error_exit "Package signing failed"
	fi
}

# Sync packages to repositories
sync_packages() {
	if [ "$SKIP_SYNC" = true ]; then
		log WARN "Skipping package sync (--skip-sync specified)"
		return 0
	fi

	log INFO "Syncing packages to repositories..."

	if sh ~/bin/packagesync.sh --sync=alpha; then
		log SUCCESS "Package sync completed"
	else
		log WARN "Package sync encountered issues (continuing anyway)"
	fi
}

# Generate build summary
generate_summary() {
	log INFO "================================"
	log SUCCESS "Daily Alpha Build Completed!"
	log INFO "PostgreSQL Version: ${pgAlphaVersion}"
	log INFO "Build Type: ${BUILD_TYPE}"
	log INFO "RPM Directory: ${RPM_BASE_DIR}"
	log INFO "================================"
}

#########################################################
# Main execution
#########################################################

main() {
	local start_time=$(date '+%s')

	# Parse command line arguments
	VERBOSE=false
	SKIP_CLEANUP=false
	SKIP_SYNC=false

	while [ $# -gt 0 ]; do
		case "$1" in
			-h|--help)
				usage
				;;
			-v|--verbose)
				VERBOSE=true
				shift
				;;
			--skip-cleanup)
				SKIP_CLEANUP=true
				shift
				;;
			--skip-sync)
				SKIP_SYNC=true
				shift
				;;
			*)
				echo "${red}ERROR:${reset} Unknown option: $1"
				echo "Use --help for usage information"
				exit 1
				;;
		esac
	done

	log INFO "Starting daily PostgreSQL ${pgAlphaVersion} alpha build..."
	log INFO "Timestamp: $(date)"

	# Execute build steps
	check_prerequisites
	prepare_build_environment
	prepare_postgresql_source
	build_postgresql_packages
	clean_old_packages
	sign_rpm_packages
	sync_packages
	generate_summary

	# Calculate execution time
	local end_time=$(date '+%s')
	local duration=$((end_time - start_time))
	local minutes=$((duration / 60))
	local seconds=$((duration % 60))

	log SUCCESS "Total execution time: ${minutes}m ${seconds}s"
}

# Run main function with all arguments
main "$@"

exit 0
