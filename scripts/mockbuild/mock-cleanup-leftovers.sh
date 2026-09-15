#!/usr/bin/env bash
#
# mock-cleanup-leftovers.sh [--apply]
#
# `sudo mock --scrub-all-chroots` cleans up ordinary stale mock chroots, but
# its cleanup is a directory-name heuristic that can't always tell where a
# --uniqueext suffix starts -- for our PGDG configs, config_opts['root'] is
# the SAME for every PG version of a given distro (e.g. every
# pgdg-opensuse-leap-16-pgNN-x86_64 config shares root
# 'pgdg-opensuse-leap-16-x86_64'), so a leftover uniqueext chroot like
# pgdg-opensuse-leap-16-x86_64-pg_qualstats gets reported as
# "Unknown directory" and left behind. mock-build-matrix.sh's -u/--unique-ext
# (used by mock-build-all.sh for safe cross-package parallelism, see its
# header comment) is exactly what creates these.
#
# This script asks mock itself for each distro's real root (via
# `mock -r <cfg> --print-root-path`, not a name guess), finds every
# <root>-<ext> and <root>-bootstrap-<ext> leftover under /var/lib/mock, and
# scrubs each properly via `mock -r <cfg> --uniqueext=<ext> --scrub=all`
# (mock's own teardown, so bind mounts etc. are unmounted correctly rather
# than us guessing at a raw rm -rf). Ordinary un-suffixed chroots are left
# alone -- run `sudo mock --scrub-all-chroots` yourself for those.
#
# Distro list and each distro's representative PG-version config come from
# mock-build-matrix.sh's own DISTROS array (assumed to sit alongside this
# script), so this stays in sync automatically when a distro is added there.
#
# Defaults to a dry run -- pass --apply to actually scrub anything.

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MATRIX_SCRIPT="$SCRIPT_DIR/mock-build-matrix.sh"

APPLY=0
if [ "${1:-}" = "--apply" ]; then
    APPLY=1
elif [ "${1:-}" = "-h" ] || [ "${1:-}" = "--help" ]; then
    echo "Usage: $0 [--apply]  (default: dry run, only prints what would be scrubbed)" >&2
    exit 1
fi

DISTROS=(fedora-43 fedora-44 rocky-9 rocky-10 opensuse-leap-15.6 opensuse-leap-16)
if [ -f "$MATRIX_SCRIPT" ]; then
    parsed="$(grep -E '^DISTROS=\(' "$MATRIX_SCRIPT" | head -1)"
    [ -n "$parsed" ] && eval "$parsed"
fi

any_found=0
for distro in "${DISTROS[@]}"; do
    cfg=""
    for pgver in 18 17 16 15 14; do
        candidate="/etc/mock/pgdg-${distro}-pg${pgver}-x86_64.cfg"
        if [ -f "$candidate" ]; then
            cfg="pgdg-${distro}-pg${pgver}-x86_64"
            break
        fi
    done
    if [ -z "$cfg" ]; then
        echo "No pgdg-${distro}-pg*-x86_64 config found under /etc/mock -- skipping $distro." >&2
        continue
    fi

    root_path="$(sudo mock -r "$cfg" --print-root-path 2>/dev/null)"
    root="$(basename "$(dirname "$root_path")")"
    if [ -z "$root" ]; then
        echo "Could not resolve root path for $cfg -- skipping $distro." >&2
        continue
    fi

    exts=()
    for d in /var/lib/mock/"$root"-*; do
        [ -d "$d" ] || continue
        base="$(basename "$d")"
        # "$root-bootstrap" itself (no further suffix) is the ordinary shared
        # bootstrap chroot every normal build uses -- not a --uniqueext leftover.
        if [ "$base" = "$root-bootstrap" ]; then
            continue
        elif [[ "$base" == "$root-bootstrap-"* ]]; then
            exts+=("${base#"$root"-bootstrap-}")
        elif [[ "$base" == "$root-"* ]]; then
            exts+=("${base#"$root"-}")
        fi
    done
    # dedupe (chroot and bootstrap dirs for the same ext both land here)
    if [ "${#exts[@]}" -gt 0 ]; then
        readarray -t exts < <(printf '%s\n' "${exts[@]}" | sort -u)
    fi

    for ext in "${exts[@]}"; do
        any_found=1
        if [ "$APPLY" -eq 1 ]; then
            echo "Scrubbing $cfg --uniqueext=$ext (root: $root)"
            sudo mock -r "$cfg" --uniqueext="$ext" --scrub=all
        else
            echo "[dry run] would scrub $cfg --uniqueext=$ext (root: $root)"
        fi
    done
done

if [ "$any_found" -eq 0 ]; then
    echo "No leftover --uniqueext chroots found under any known PGDG root."
elif [ "$APPLY" -eq 0 ]; then
    echo
    echo "Dry run only -- re-run with --apply to actually scrub the above."
fi

echo
echo "Note: this only handles our own --uniqueext leftovers. For ordinary stale"
echo "chroots (no uniqueext), run: sudo mock --scrub-all-chroots"
