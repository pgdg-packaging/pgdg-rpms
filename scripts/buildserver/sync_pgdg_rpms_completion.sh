# Bash completion for sync_pgdg_rpms.sh

_sync_pgdg_rpms() {
	local cur prev opts os_choice

	COMPREPLY=()
	cur="${COMP_WORDS[COMP_CWORD]}"
	prev="${COMP_WORDS[COMP_CWORD - 1]}"

	opts="--os --arch --ver --dry-run --debug --help"

	# Extract --os value if provided
	for i in "${!COMP_WORDS[@]}"; do
		if [[ "${COMP_WORDS[i]}" == "--os" && -n "${COMP_WORDS[i + 1]}" ]]; then
			os_choice="${COMP_WORDS[i + 1]}"
		fi
	done

	case "$prev" in
	--os)
		COMPREPLY=($(compgen -W "redhat fedora" -- "$cur"))
		return 0
		;;
	--arch)
		COMPREPLY=($(compgen -W "aarch64 ppc64le x86_64" -- "$cur"))
		return 0
		;;
	--ver)
		if [[ "$os_choice" == "redhat" ]]; then
			COMPREPLY=($(compgen -W "10 9 8 7" -- "$cur"))
		elif [[ "$os_choice" == "fedora" ]]; then
			COMPREPLY=($(compgen -W "42 41" -- "$cur"))
		fi
		return 0
		;;
	esac

	if [[ "$cur" == --* ]]; then
		COMPREPLY=($(compgen -W "$opts" -- "$cur"))
	fi
}

# Register the function for your script name
complete -F _sync_pgdg_rpms sync_pgdg_rpms.sh
