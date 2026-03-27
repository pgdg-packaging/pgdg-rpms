#!/usr/bin/bash

# Bash completion for aws_sync_archive.sh

_aws_sync_archive_completions() {
    local cur prev opts
    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"

    # Source config directly so its arrays are available in this scope
    local script_dir
    script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    # shellcheck source=aws_sync_config.sh
    source "$script_dir/aws_sync_config.sh"

    local os_names="fedora opensuse redhat sles"
    local archs="${VALID_ARCH[*]}"
    local redhat_os_versions="${VALID_REDHAT_OS_VERSIONS[*]}"
    local fedora_os_versions="${VALID_FEDORA_OS_VERSIONS[*]}"
    local sles_os_versions="${VALID_SLES_OS_VERSIONS[*]}"
    local opensuse_os_versions="${VALID_OPENSUSE_OS_VERSIONS[*]}"
    local pg_versions="${VALID_PG_VERSIONS[*]}"

    opts="--os-name --arch --os-version --pg-version --extras --non-free --dry-run --debug --help"

    case "$prev" in
        --os-name)
            COMPREPLY=( $(compgen -W "${os_names}" -- "$cur") )
            return 0
            ;;
        --arch)
            COMPREPLY=( $(compgen -W "${archs}" -- "$cur") )
            return 0
            ;;
        --os-version)
            # Offer version list matching --os-name if already specified
            local os_name_val=""
            for ((i=1; i < COMP_CWORD; i++)); do
                if [[ "${COMP_WORDS[i]}" == "--os-name" ]]; then
                    os_name_val="${COMP_WORDS[i+1]}"
                    break
                fi
            done
            if [[ "$os_name_val" == "redhat" ]]; then
                COMPREPLY=( $(compgen -W "${redhat_os_versions}" -- "$cur") )
            elif [[ "$os_name_val" == "fedora" ]]; then
                COMPREPLY=( $(compgen -W "${fedora_os_versions}" -- "$cur") )
            elif [[ "$os_name_val" == "sles" ]]; then
                COMPREPLY=( $(compgen -W "${sles_os_versions}" -- "$cur") )
            elif [[ "$os_name_val" == "opensuse" ]]; then
                COMPREPLY=( $(compgen -W "${opensuse_os_versions}" -- "$cur") )
            else
                # os-name not yet specified — offer all versions
                COMPREPLY=( $(compgen -W "${redhat_os_versions} ${fedora_os_versions} ${sles_os_versions} ${opensuse_os_versions}" -- "$cur") )
            fi
            return 0
            ;;
        --pg-version)
            COMPREPLY=( $(compgen -W "${pg_versions}" -- "$cur") )
            return 0
            ;;
        --extras)
            COMPREPLY=( $(compgen -W "1" -- "$cur") )
            return 0
            ;;
        *)
            ;;
    esac

    # Default: complete option names
    COMPREPLY=( $(compgen -W "${opts}" -- "$cur") )
    return 0
}

complete -F _aws_sync_archive_completions aws_sync_archive.sh
