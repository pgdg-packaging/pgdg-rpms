# sync_pgdg_rpms — Documentation

## Overview

This suite of Bash scripts automates the synchronisation of PostgreSQL Global Development Group (PGDG) RPM packages from upstream build hosts to a local mirror. It supports Red Hat Enterprise Linux (RHEL), Fedora, SUSE Linux Enterprise Server (SLES), and openSUSE Leap, and is designed to be run manually or via a cron job.

The suite consists of five files:

| File | Purpose |
|---|---|
| `sync_pgdg_rpms_config.sh` | Central configuration — sourced by all other scripts |
| `sync_pgdg_rpms.sh` | Main sync script — drives rsync for a given OS, version, and architecture |
| `sync_pgdg_rpms_cron.sh` | Cron wrapper — iterates over all OS/version combinations and calls the main script |
| `sync_pgdg_rpms_completion.sh` | Bash tab-completion — provides context-aware completions for the main script |
| `sync_pgdg_rpms_reporpms.sh` | Republishes the latest `pgdg-redhat-repo`/`pgdg-fedora-repo` RPM and its `-latest` symlink after a sync |

---

## Architecture

```
sync_pgdg_rpms_config.sh       ← Single source of truth for all settings
        │
        ├── sync_pgdg_rpms.sh          ← Manual/targeted sync
        │
        ├── sync_pgdg_rpms_cron.sh     ← Full automated sync (cron)
        │
        └── sync_pgdg_rpms_reporpms.sh ← Republish latest repo RPM + symlink

sync_pgdg_rpms_completion.sh   ← Bash completion (sourced in shell profile)
```

All scripts begin by locating and sourcing `sync_pgdg_rpms_config.sh` from the same directory as the calling script. If the config file is missing, they exit immediately with an error.

---

## Configuration (`sync_pgdg_rpms_config.sh`)

This file is the single source of truth for all settings shared across the suite. It must reside in the same directory as the other scripts.

### PostgreSQL Versions

| Variable | Value | Description |
|---|---|---|
| `PG_ALL_VERSIONS` | `(18 17 16 15 14)` | All supported stable PG versions |
| `PG_TEST_VERSIONS` | `(20 19 18 17 16 15 14)` | Versions available in testing repos |

### Supported Operating Systems

`VALID_OS=("redhat" "fedora" "sles" "opensuse")`

### Architectures per OS

| OS | Supported Architectures |
|---|---|
| `redhat` | `aarch64`, `ppc64le`, `x86_64` |
| `fedora` | `x86_64` |
| `sles` | `x86_64` |
| `opensuse` | `x86_64` |

### Per-Version Architecture Overrides

Not every OS version necessarily ships every architecture listed above — e.g. a brand-new RHEL release may ship `x86_64` packages before `aarch64`/`ppc64le` catch up. `VALID_ARCH_OVERRIDES` is an associative array keyed `"<os>:<ver>"` that restricts the architecture list for just that one version; any `os:ver` pair not listed there falls back to the full `VALID_ARCH_<os>` list unchanged:

```bash
declare -A VALID_ARCH_OVERRIDES=(
	[redhat:10.0]="x86_64 aarch64"    # ppc64le not yet available for 10.0
)
```

Both `sync_pgdg_rpms.sh` and `sync_pgdg_rpms_reporpms.sh` resolve the architecture list per OS/version pair via the `get_valid_arch_for` helper (also defined in the config file), so an override here is picked up automatically by both — no other changes required. A `--arch` that doesn't apply to a given version is skipped quietly (shown with `--debug`), except when both `--os` and `--ver` are given explicitly together with an explicit `--arch` in `sync_pgdg_rpms.sh`, where a mismatch is still a hard error since exactly one target was requested.

### Versions per OS

| OS | Supported Versions |
|---|---|
| `redhat` | `10.2`, `10.1`, `10.0`, `9.8`, `9.7`, `9.6`, `8.10` |
| `fedora` | `44`, `43` |
| `sles` | `15.6`, `15.7`, `16.0` |
| `opensuse` | `16.0` |

### Base Directories

| OS | Local Base Path |
|---|---|
| `redhat` | `/srv/yum/yum` |
| `fedora` | `/srv/yum/yum` |
| `sles` | `/srv/zypp/zypp` |
| `opensuse` | `/srv/zypp/zypp` |

### Feature Flags per OS

These flags control which optional repo types are enabled by default when no `--sync` argument is passed.

| Flag | redhat | fedora | sles | opensuse |
|---|---|---|---|---|
| `EXTRASREPOSENABLED` | 1 | 0 | 1 | 1 |
| `SYNCTESTINGREPOS` | 1 | 1 | 0 | 0 |
| `SYNCNONFREEREPOS` | 1 | 0 | 0 | 0 |

### Non-Free Availability

`SYNCNONFREEREPOS_<os>` above only controls whether non-free is attempted *at all* by default for an OS. Even where it's enabled, the actual non-free repo only exists for a limited subset of versions and architectures, tracked separately via `VALID_NONFREE_VER_<os>` and `VALID_NONFREE_ARCH_<os>`:

| OS | Non-Free Versions | Non-Free Architectures |
|---|---|---|
| `redhat` | `10.2`, `10.1`, `9.8`, `9.7`, `8.10` | `x86_64` |
| `fedora` | *(none)* | *(none)* |
| `sles` | *(none)* | *(none)* |
| `opensuse` | *(none)* | *(none)* |

`sync_pgdg_rpms.sh` checks both lists for every OS/version/arch combination before attempting a non-free rsync; a combination not listed (e.g. RHEL `10.0`/`9.6`, or any `aarch64`/`ppc64le` target) is skipped quietly (visible with `--debug`) rather than attempted and failed.

### OS Naming

| OS key | `OSNAME` | `OSDISTRO` |
|---|---|---|
| `redhat` | `rhel` | `redhat` |
| `fedora` | `fedora` | `fedora` |
| `sles` | `sles` | `suse` |
| `opensuse` | `leap` | `opensuse` |

---

## Main Sync Script (`sync_pgdg_rpms.sh`)

### Usage

```bash
./sync_pgdg_rpms.sh [--os <os>] [--ver <version>] [--arch <arch>] [--sync <items...>] [--dry-run] [--debug]
```

### Options

| Option | Required | Description |
|---|---|---|
| `--os` | No | Operating system: `redhat`, `fedora`, `sles`, or `opensuse`. If omitted, all supported operating systems are synced |
| `--ver` | No | OS version (e.g. `9.7`, `15.6`, `43`). If omitted, all valid versions for the OS(es) being processed are synced |
| `--arch` | No | Architecture: `aarch64`, `ppc64le`, or `x86_64`. If omitted, all supported architectures for the OS(es) being processed are synced |
| `--sync` | No | One or more items to sync: `common`, `extras`, `testing`, `non-free`, or a PG version number (e.g. `17`). Multiple values accepted. If omitted, all available repos are synced |
| `--dry-run` | No | Print what would be synced without executing rsync |
| `--debug` | No | Print detailed internal variable state before syncing |

When `--os` is omitted, the script loops over every OS in `VALID_OS`. In that case a `--ver` or `--arch` value that doesn't apply to a given OS (e.g. `--ver 16.0` doesn't exist for `redhat`) simply skips that OS rather than erroring out — the skip is only visible with `--debug`. When `--os` is given explicitly, an invalid `--ver`/`--arch` for that OS is still treated as a hard error, as before.

### Sync Items

| Item | Description |
|---|---|
| `common` | OS-independent common packages (`/var/lib/pgsql/rpmcommon/ALLRPMS`) |
| `extras` | Extra packages (`/var/lib/pgsql/pgdg.extras/ALLRPMS`) |
| `testing` | Testing repos — both common testing and per-version testing trees |
| `non-free` | Non-free packages (`/var/lib/pgsql/nonfree/ALLRPMS`) |
| `17`, `18`, … | Specific PG version packages (`/var/lib/pgsql/rpm<ver>/ALLRPMS`) |

### Source Host Naming Convention

The script constructs the rsync source hostname dynamically:

| OS | Pattern |
|---|---|
| `redhat` | `pgrpms-el<ver>-<arch>.postgresql.org` |
| `fedora` | `pgrpms-fedora<ver>-<arch>.postgresql.org` |
| `sles` | `pgrpms-sles<ver>-<arch>.postgresql.org` |
| `opensuse` | `pgrpms-opensuse<ver>-<arch>.postgresql.org` |

### Local Destination Directory Structure

```
<BASE_DIR_OS>/
├── <pg_version>/           # e.g. 17/
│   └── <osdistro>/
│       └── <osname>-<ver>-<arch>/
├── common/
│   └── <osdistro>/
│       └── <osname>-<ver>-<arch>/
├── extras/
│   └── <osdistro>/
│       └── <osname>-<ver>-<arch>/
├── testing/
│   ├── common/
│   │   └── <osdistro>/
│   │       └── <osname>-<ver>-<arch>/
│   └── <pg_version>/
│       └── <osdistro>/
│           └── <osname>-<ver>-<arch>/
└── nonfree/
    └── <osdistro>/
        └── <osname>-<ver>-<arch>/
```

### Examples

```bash
# Sync only the common repo for RHEL 9.7
./sync_pgdg_rpms.sh --os redhat --ver 9.7 --sync common

# Sync PG 18 and PG 17 for SLES 15.6, x86_64 only
./sync_pgdg_rpms.sh --os sles --ver 15.6 --arch x86_64 --sync 18 17

# Sync common, extras, and testing repos for Fedora 43
./sync_pgdg_rpms.sh --os fedora --ver 43 --sync common extras testing

# Dry-run: see what would be synced for all RHEL versions
./sync_pgdg_rpms.sh --os redhat --dry-run

# Sync everything for all RHEL versions and all architectures
./sync_pgdg_rpms.sh --os redhat

# Sync just the common repo across every supported OS and version
./sync_pgdg_rpms.sh --sync common
```

### Error Handling

Each rsync call is wrapped in an error check. If any individual rsync fails, the error is reported to stderr and a flag (`sync_had_errors=1`) is set. The script continues processing remaining targets rather than aborting. At the end, if any errors occurred, the script exits with code `1` and a warning message. If all syncs succeeded, it exits with code `0`.

---

## Cron Wrapper (`sync_pgdg_rpms_cron.sh`)

This script is intended to be called by cron to perform a full, unattended sync of all configured OS/version combinations. It delegates the actual sync work to `sync_pgdg_rpms.sh`, which handles all architectures automatically.

### Usage

```bash
./sync_pgdg_rpms_cron.sh [--dry-run] [--debug] [--sync item1 item2 ...]
```

### Options

| Option | Description |
|---|---|
| `--dry-run` | Passed through to `sync_pgdg_rpms.sh` |
| `--debug` | Passed through to `sync_pgdg_rpms.sh` |
| `--sync` | Passed through to `sync_pgdg_rpms.sh` to limit what is synced |

### Behaviour

1. Sources `sync_pgdg_rpms_config.sh` to read all OS/version mappings.
2. Builds an associative array (`OS_VERSIONS`) mapping each OS to its list of versions.
3. Iterates over every `os → version` pair and invokes `sync_pgdg_rpms.sh --os <os> --ver <ver>`.
4. If a particular `os/ver` combination fails, logs the error and continues with the next (using `|| continue`).
5. Logs all actions with timestamps via a `log()` helper.

### Suggested Crontab Entry

```cron
# Run full PGDG RPM sync nightly at 02:00
0 2 * * * /path/to/sync_pgdg_rpms_cron.sh >> /var/log/pgdg_sync.log 2>&1
```

---

## Repo RPM Republisher (`sync_pgdg_rpms_reporpms.sh`)

After a sync, the `pgdg-redhat-repo` and `pgdg-fedora-repo` RPMs (the packages that install the PGDG yum repo definitions) live in the freshly-synced `common` trees. This script finds the newest one for each OS/version/arch and republishes it under a dedicated `reporpms` tree so it can be served from a stable, predictable path.

### Usage

```bash
./sync_pgdg_rpms_reporpms.sh [--os <os>] [--ver <version>] [--arch <arch>] [--dry-run] [--debug]
```

### Options

| Option | Required | Description |
|---|---|---|
| `--os` | No | Restrict to one OS: `redhat` or `fedora` (default: both) |
| `--ver` | No | Restrict to one OS version (must be valid for `--os`) |
| `--arch` | No | Restrict to one architecture (must be valid for `--os`) |
| `--dry-run` | No | Show what would change without touching any files |
| `--debug` | No | Show detailed debug output |

Only `redhat` and `fedora` are supported — `sles` and `opensuse` have no equivalent repo-RPM concept in this workflow.

### Behaviour

For every `os`/`ver`/`arch` combination:

1. Looks in `<BASE_DIR_OS>/common/<os>/<osname>-<ver>-<arch>` for the highest-versioned `<reponame>-*.rpm` (sorted with `sort -V`).
2. If it isn't already present in `<BASE_DIR_OS>/reporpms/EL-<ver>-<arch>` (redhat) or `.../F-<ver>-<arch>` (fedora), copies it in.
3. Re-points the `<reponame>-latest.noarch.rpm` symlink at the new RPM.
4. Removes any other file or symlink in the destination matching `<reponame>-*` (older versioned RPMs, stray symlinks, etc.), so the destination only ever holds the current RPM plus the `-latest` symlink.
5. Skips a combination cleanly (no error) if the source `common` directory doesn't exist yet; warns and flags an error if the destination `reporpms` directory is missing.

Like the main sync script, failures are collected rather than aborting the run: it exits `1` with a warning if any update failed, `0` if everything is up to date.

### Suggested Crontab Entry

Run after the nightly sync so the repo RPMs reflect what was just synced:

```cron
# Republish repo RPMs shortly after the nightly sync completes
30 2 * * * /path/to/sync_pgdg_rpms_reporpms.sh >> /var/log/pgdg_reporpms.log 2>&1
```

---

## Bash Completion (`sync_pgdg_rpms_completion.sh`)

This file provides context-aware tab completion for `sync_pgdg_rpms.sh`.

### Installation

Source the file in your shell profile or completions directory:

```bash
# Add to ~/.bashrc or /etc/bash_completion.d/
source /path/to/sync_pgdg_rpms_completion.sh
```

### Completion Behaviour

| Context | Completions offered |
|---|---|
| After `--os` | `redhat`, `fedora`, `sles`, `opensuse` |
| After `--ver` | Valid versions for the selected `--os` (or all versions if `--os` not yet given) |
| After `--arch` | Valid architectures for the selected `--os` (or all architectures) |
| After `--sync` | `common`, `extras`, `testing`, `non-free`, and all PG versions from `PG_ALL_VERSIONS` |
| Continuing `--sync` values | Same as above (multi-value support) |
| Default / `--` prefix | `--os`, `--arch`, `--ver`, `--sync`, `--dry-run`, `--debug` |

The completion function attempts to load `sync_pgdg_rpms_config.sh` automatically to keep completions in sync with the live configuration. If the config file cannot be found, it falls back to hardcoded values.

---

## Deployment Checklist

1. Place all five scripts in the same directory.
2. Ensure `sync_pgdg_rpms_config.sh` is readable by the user running the sync.
3. Make `sync_pgdg_rpms.sh`, `sync_pgdg_rpms_cron.sh`, and `sync_pgdg_rpms_reporpms.sh` executable: `chmod +x sync_pgdg_rpms.sh sync_pgdg_rpms_cron.sh sync_pgdg_rpms_reporpms.sh`
4. Verify SSH connectivity from the sync host to each upstream build host (`pgrpms-*.postgresql.org`) without a passphrase prompt (use SSH keys and `ssh-agent` or an `authorized_keys` entry).
5. Confirm the local base directories (`/srv/yum/yum`, `/srv/zypp/zypp`) exist and are writable, including the `reporpms/EL-<ver>-<arch>` and `reporpms/F-<ver>-<arch>` destination directories used by `sync_pgdg_rpms_reporpms.sh`.
6. Test with `--dry-run` before running live.
7. Source `sync_pgdg_rpms_completion.sh` in your shell profile for tab completion.
8. Add `sync_pgdg_rpms_cron.sh` to crontab for automated nightly syncs, and `sync_pgdg_rpms_reporpms.sh` shortly after it.

---

## Adding New PG Versions or OS Versions

All changes should be made exclusively in `sync_pgdg_rpms_config.sh`:

- **New PG version** — add the version number to both `PG_ALL_VERSIONS` and `PG_TEST_VERSIONS`.
- **New OS version** — add the version string to the relevant `VALID_VER_<os>` array. For `redhat`/`fedora`, also create the matching `reporpms/EL-<ver>-<arch>` or `reporpms/F-<ver>-<arch>` destination directories, since `sync_pgdg_rpms_reporpms.sh` reads `VALID_VER_<os>` directly from the config and will warn (and flag an error) if the destination is missing. If the new version doesn't ship every architecture in `VALID_ARCH_<os>` yet, add a `VALID_ARCH_OVERRIDES["<os>:<ver>"]` entry restricting it to the architectures that actually exist (see "Per-Version Architecture Overrides" above) — otherwise both scripts will attempt (and fail or warn on) architectures that don't exist for that version. If the new version also has a non-free repo, add it to `VALID_NONFREE_VER_<os>` (see "Non-Free Availability" above) — it is *not* picked up automatically just by being in `VALID_VER_<os>`.
- **New OS** — add the OS name to `VALID_OS`, create `VALID_ARCH_<os>`, `VALID_VER_<os>`, `BASE_DIR_<os>`, `OSNAME_<os>`, `OSDISTRO_<os>`, the three feature flag variables (`EXTRASREPOSENABLED_<os>`, `SYNCTESTINGREPOS_<os>`, `SYNCNONFREEREPOS_<os>`), and `VALID_NONFREE_VER_<os>`/`VALID_NONFREE_ARCH_<os>` (empty arrays if the OS has no non-free repo). Then add a matching `elif` branch in `sync_pgdg_rpms.sh` for `SOURCE_HOST` and `NONFREE_SOURCE_HOST`, add the OS to `OS_VERSIONS` in `sync_pgdg_rpms_cron.sh`, and extend the fallback arrays and completion cases in `sync_pgdg_rpms_completion.sh`. (`VALID_ARCH_<os>`/`VALID_VER_<os>` themselves are picked up automatically via nameref — no per-OS `case` block needed for those.)

---

## Rsync Flags Reference

All rsync calls use the following flags:

| Flag | Meaning |
|---|---|
| `-a` | Archive mode (preserves permissions, timestamps, symlinks, etc.) |
| `-v` | Verbose output |
| `-e ssh` | Use SSH as the transport |
| `--delete` | Remove files from the destination that no longer exist at the source |
| `--delete-missing-args` | Delete destination files if the source path itself is missing |
