# PostgreSQL YUM Repository S3 Sync Scripts

These scripts sync PostgreSQL YUM repository packages from a local mirror directory to the `s3://yum-archive.postgresql.org` S3 bucket. They are designed to be run after a new OS version, PostgreSQL version, or architecture is added to the local mirror, and handle both targeted single-repo syncs and bulk archive-wide syncs.

## Files

| File | Purpose |
|------|---------|
| `aws_sync_config.sh` | Shared configuration: valid values and the `is_valid()` helper. Sourced by all other scripts. |
| `aws_sync.sh` | Low-level sync script. Syncs one OS/version combination across one or all architectures. |
| `aws_sync_archive.sh` | High-level wrapper. Iterates over OS versions and PG versions, calling `aws_sync.sh` for each combination. |
| `aws_sync_archive_completion.sh` | Bash tab-completion for `aws_sync_archive.sh`. |

All scripts must live in the **same directory** — they resolve each other's paths via `BASH_SOURCE[0]`.

---

## Configuration — `aws_sync_config.sh`

Defines all valid values used for validation across the suite. Edit this file when adding new OS versions, PG versions, or architectures — no other script needs changing.

```bash
VALID_ARCH=("aarch64" "ppc64le" "x86_64")
VALID_PG_VERSIONS=(13 14 15 16 17 18)
VALID_REDHAT_OS_VERSIONS=(7 8.10 9.6 9.7 10.0 10.1)
VALID_FEDORA_OS_VERSIONS=(41 42 43)
VALID_SLES_OS_VERSIONS=(12.5 15.6 15.7 16.0)
VALID_OPENSUSE_OS_VERSIONS=(16.0)

# Base directories per OS distro
BASE_DIR_redhat="/srv/yum/yum"
BASE_DIR_fedora="/srv/yum/yum"
BASE_DIR_suse="/srv/zypp/zypp"
BASE_DIR_opensuse="/srv/zypp/zypp"

# Non-free repo base directory (redhat only)
BASE_DIR_non_free="/srv/yum/yum/non-free"

# S3 bucket per OS distro
S3_BUCKET_redhat="s3://yum-archive.postgresql.org"
S3_BUCKET_fedora="s3://yum-archive.postgresql.org"
S3_BUCKET_suse="s3://zypp-archive.postgresql.org"
S3_BUCKET_opensuse="s3://zypp-archive.postgresql.org"
```

Also defines `is_valid()`, a helper used by other scripts for safe exact-match validation (avoids regex dot-wildcard issues with dotted version strings like `9.6`).

---

## `aws_sync.sh` — Single OS/Version Sync

The core sync script. Given an OS and version, it syncs either the **common repo** (if `--pg` is omitted) or a **specific PG version repo** (if `--pg` is provided). It loops over all architectures unless `--arch` pins it to one.

After a successful sync it automatically removes any corresponding **testing repo** directories from the local mirror for each synced architecture.

### Local directory layout expected

```
/srv/yum/yum/
├── common/
│   └── redhat/
│       └── rhel-9.6-x86_64/
├── 16/
│   └── redhat/
│       └── rhel-9.6-x86_64/
├── testing/
│   └── 16/
│       └── redhat/
│           └── rhel-9.6-x86_64/   ← removed after sync
└── extras/
    └── redhat/
        └── x86_64/
```

### Usage

```
aws_sync.sh --os <os> --ver <version> [--arch <arch>] [--pg <pg_version>] [options]
```

### Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--os` | Yes | OS type: `rhel`, `fedora`, `sles`, or `opensuse` |
| `--ver` | Yes | OS version, e.g. `9.6`, `10.0`, `42` |
| `--arch` | No | Architecture: `aarch64`, `ppc64le`, `x86_64`. If omitted, all three are synced. |
| `--pg` | No | PostgreSQL major version, e.g. `16`. If omitted, the common repo is synced instead. |
| `--extras=1` | No | Also sync the extras repo (redhat only). |
| `--non-free` | No | Sync non-free repos for all PG versions (redhat only). |
| `--dry-run` | No | Print what would be run without executing anything. |
| `--debug` | No | Print resolved parameter values before running. |

### Examples

Sync the common repo for RHEL 9.6, all architectures:
```bash
aws_sync.sh --os rhel --ver 9.6
```

Sync PG 16 for RHEL 9.6, x86_64 only:
```bash
aws_sync.sh --os rhel --ver 9.6 --pg 16 --arch x86_64
```

Sync PG 17 for Fedora 42, all architectures, dry run:
```bash
aws_sync.sh --os fedora --ver 42 --pg 17 --dry-run
```

Sync PG 16 for RHEL 10.0, all architectures, including extras:
```bash
aws_sync.sh --os rhel --ver 10.0 --pg 16 --extras=1
```

Sync PG 16 for SLES 15.6, all architectures:
```bash
aws_sync.sh --os sles --ver 15.6 --pg 16
```

Sync PG 16 for RHEL 9.6 including non-free repos:
```bash
aws_sync.sh --os rhel --ver 9.6 --pg 16 --non-free
```
Sync the common repo for SLES 15.7, x86_64 only, dry run:
```bash
aws_sync.sh --os sles --ver 15.7 --arch x86_64 --dry-run
```

Sync PG 16 for openSUSE Leap 16.0, all architectures:
```bash
aws_sync.sh --os opensuse --ver 16.0 --pg 16
```

### What it does, step by step

1. Validates `--os`, `--arch` (if given), and `--pg` (if given) against the config arrays.
2. Resolves the arch list: the provided value, or all of `VALID_ARCH`.
3. For each architecture:
   - If `--pg` was omitted → syncs `common/<osdistro>/<os>-<ver>-<arch>/` to S3.
   - If `--pg` was provided → syncs `<pg>/<osdistro>/<os>-<ver>-<arch>/` to S3.
   - If any sync succeeded → removes `testing/[common/|debug/]<pgver>/<osdistro>/<os>-<ver>-<arch>/` for every PG version.
   - If `--extras=1` → syncs `extras/<osdistro>/<arch>/` to S3.
4. After the arch loop, if `--non-free` → syncs `non-free/<pgver>/` to `$S3_BUCKET/non-free/<pgver>/` for every entry in `VALID_PG_VERSIONS` (redhat only; local root: `/srv/yum/yum/non-free/`).

---

## `aws_sync_archive.sh` — Bulk Sync Wrapper

A higher-level script that drives `aws_sync.sh` across multiple OS versions and PG versions in one invocation. Each dimension (`--os-version`, `--pg-version`, `--arch`) is optional; omitting one causes that dimension to expand to all valid values.

Arch expansion is delegated entirely to `aws_sync.sh`, so `aws_sync_archive.sh` only loops over OS versions and PG versions.

### Usage

```
aws_sync_archive.sh --os-name <fedora|redhat> [--arch <arch>] [--os-version <ver>] [--pg-version <pg>] [options]
```

### Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--os-name` | Yes | `redhat`, `fedora`, `sles`, or `opensuse` |
| `--arch` | No | Pin to one architecture. If omitted, all architectures are synced (via `aws_sync.sh`). |
| `--os-version` | No | Pin to one OS version. If omitted, all valid versions for the OS are used. |
| `--pg-version` | No | Pin to one PG major version. If omitted, all versions in `VALID_PG_VERSIONS` are used. |
| `--extras=1` | No | Pass through to `aws_sync.sh` (redhat only). |
| `--non-free` | No | Pass through to `aws_sync.sh`; sync non-free repos for all PG versions (redhat only). Rejected with an error if `--os-name` is not `redhat`. |
| `--dry-run` | No | Passed through to `aws_sync.sh`. |
| `--debug` | No | Passed through to `aws_sync.sh`. |

When either `--os-version` or `--pg-version` is omitted the script will prompt for confirmation before proceeding, since this can result in a large number of sync operations.

Failed invocations of `aws_sync.sh` are logged to `aws_sync_archive_failures.log` in the same directory as the scripts rather than aborting the entire run, so a single failure doesn't prevent other combinations from syncing.

### Examples

Sync all PG versions for all RHEL OS versions, all architectures (will prompt for confirmation):
```bash
aws_sync_archive.sh --os-name redhat
```

Sync PG 16 across all RHEL versions, x86_64 only:
```bash
aws_sync_archive.sh --os-name redhat --pg-version 16 --arch x86_64
```

Sync all PG versions for Fedora 42, dry run:
```bash
aws_sync_archive.sh --os-name fedora --os-version 42 --dry-run
```

Sync PG 17 for RHEL 9.6, all architectures, with extras:
```bash
aws_sync_archive.sh --os-name redhat --os-version 9.6 --pg-version 17 --extras=1
```

Sync all PG versions for all SLES OS versions, all architectures (will prompt for confirmation):
```bash
aws_sync_archive.sh --os-name sles
```

Sync PG 16 for SLES 15.6, x86_64 only:
```bash
aws_sync_archive.sh --os-name sles --os-version 15.6 --pg-version 16 --arch x86_64
```

Sync all PG versions for openSUSE Leap 16.0, all architectures:
```bash
aws_sync_archive.sh --os-name opensuse --os-version 16.0
```

Sync all PG versions for RHEL 9.6 including non-free repos:
```bash
aws_sync_archive.sh --os-name redhat --os-version 9.6 --non-free
```

---

## Tab Completion — `aws_sync_archive_completion.sh`

Provides bash tab-completion for `aws_sync_archive.sh`. It reads valid values at completion time by sourcing `aws_sync_config.sh`, so it stays automatically in sync whenever the config is updated.

### Setup

Source the file in your shell profile or in `/etc/bash_completion.d/`:

```bash
# Add to ~/.bashrc or ~/.bash_profile
source /path/to/aws_sync_archive_completion.sh
```

Or for system-wide availability:

```bash
cp aws_sync_archive_completion.sh /etc/bash_completion.d/
```

### Behaviour

- `--os-name` completes to `fedora`, `redhat`, `sles`, or `opensuse`.
- `--arch` completes from `VALID_ARCH`.
- `--os-version` completes from the appropriate version list based on whatever `--os-name` has already been typed; if `--os-name` hasn't been set yet, all OS versions are offered.
- `--pg-version` completes from `VALID_PG_VERSIONS`.
- `--extras` completes to `1`.
- All flag names are completed when typing `--`.

---

## Adding a New OS Version, PG Version, or Architecture

Edit **only** `aws_sync_config.sh`. All scripts and tab-completion pick up the change automatically.

```bash
# Example: add RHEL 10.2, PG 19, SLES 15.8, and openSUSE Leap 16.1
VALID_REDHAT_OS_VERSIONS=(7 8.10 9.6 9.7 10.0 10.1 10.2)
VALID_PG_VERSIONS=(13 14 15 16 17 18 19)
VALID_SLES_OS_VERSIONS=(12.5 15.6 15.7 15.8 16.0)
VALID_OPENSUSE_OS_VERSIONS=(16.0 16.1)
```

> **Note on dotted version strings:** validation uses exact string matching (not regex), so versions like `9.6` or `10.0` are handled safely.

---

## Prerequisites

- `aws` CLI installed and configured with credentials that have write access to `s3://yum-archive.postgresql.org`.
- Bash 4.0 or later (for associative arrays and `[[ ]]`).
- The local mirror rooted at `/srv/yum/yum/` must exist and be populated before syncing.
