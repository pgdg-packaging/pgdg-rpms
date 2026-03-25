PostgreSQL YUM Repository: Build Server Scripts
================================================

This collection of shell scripts automates building, signing, and publishing
RPM packages for the PostgreSQL YUM repository (yum.postgresql.org). The
scripts handle the full lifecycle: compiling packages with `rpmbuild`, signing
with GPG, creating repository metadata with `createrepo`, and syncing
everything to AWS S3 with CloudFront cache invalidation.

All scripts must be run as the `postgres` system user (UID 26). This is
enforced in `global.sh`, which every other script sources first.

---

## Architecture Overview

The scripts distinguish between three repository categories:

- **Common** — packages that are version-independent (e.g., shared
  utilities), stored in `rpmcommon/` and published under the `common/`
  path in S3.
- **Non-common** — packages built per PostgreSQL major version (e.g.,
  PostGIS, pgpool-II), stored in `rpm<version>/` directories.
- **Extras** — additional packages for RHEL/SLES platforms, stored in
  `pgdg.extras/`.

Separately, **non-free** packages are handled by dedicated scripts
(`packagebuildnonfree.sh`, `packagesyncnonfree.sh`) to prevent accidentally
building proprietary software on shared instances.

The S3 layout separates binary RPMs, debug packages, and SRPMs into distinct
buckets (`dnf-debuginfo`, `dnf-srpms`), each fronted by a CloudFront
distribution. SLES and openSUSE Leap builds use a parallel `zypp`-prefixed bucket set instead
of `dnf`.

---

## global.sh

The central configuration file sourced by every other script. It defines all
shared variables and the two reusable functions `sign_package` and
`preset_gpg_passphrase`.

### OS Configuration

| Variable | Example | Description |
|---|---|---|
| `osmajorversion` | `10` | OS major version (RHEL 10, SLES 15, Fedora 43) |
| `os` | `rhel-10` | Full OS string used in directory and S3 paths; use `leap-16` for openSUSE Leap |
| `osminversion` | `1` | Minor version for RHEL/SLES (e.g. RHEL 10.1) |
| `osislatest` | `0` or `1` | When `1`, packages are also synced to the major-version path (S3 has no symlinks) |
| `osarch` | `x86_64` | Architecture; also `aarch64`, `ppc64le` |
| `osdistro` | `redhat` | Distro family: `fedora`, `redhat`, `suse`, or `opensuse` |
| `git_os` | `EL-10` | Git branch suffix used in clone paths |
| `extrasrepoenabled` | `1` | Enables the extras repository for RHEL/SLES |

### PostgreSQL Build Versions

| Variable | Example | Description |
|---|---|---|
| `pgStableBuilds` | `("18 17 16 15 14")` | Production versions, used by `packagesync.sh` and `packagebuild.sh` |
| `pgTestBuilds` | `("19 18 17 16 15 14")` | Versions available in testing repos |
| `pgBetaVersion` | `()` | Current beta version (empty when no active beta) |
| `pgAlphaVersion` | `(19)` | Current alpha/development version |

### GPG Configuration

`GPG_KEY_ID` and `GPG_PASSWORD` must be set before use. The password is used
for `repomd.xml` signing (via `gpg2 --passphrase-fd`) while package signing
itself relies on `gpg-agent` with a pre-loaded passphrase (see
`gpg-setup-secure.sh`).

### AWS Configuration

`awssrpmurl` and `awsdebuginfourl` point to separate S3 buckets for SRPMs
and debug packages. `CF_SRPM_DISTRO_ID` and `CF_DEBUG_DISTRO_ID` are the
CloudFront distribution IDs that must be invalidated after every sync.
Set `AWS_PAGER=""` to suppress interactive output in automated runs.

### `sign_package <rpm_location>`

Finds all RPMs under `~/<rpm_location>*/` and signs them with `rpmsign
--addsign`. Before signing it purges any leftover `.sig` files and
`buildreqs.nosrc` packages that would otherwise break the signing process.
Requires `gpg-agent` to be running with the passphrase already preset.

### `preset_gpg_passphrase <keygrip>`

Feeds `GPG_PASSWORD` into `/usr/libexec/gpg-preset-passphrase` so the
agent can sign without prompting. On SLES 15 the binary path is
`/usr/lib/gpg-preset-passphrase`; SLES 16 uses the same path as RHEL.

### Crontab note

Add `TERM=xterm` at the top of the crontab so that the `tput` colour
definitions in `global.sh` do not produce errors in non-interactive
shells. Alternatively, guard the colour definitions:

```bash
if [ -t 1 ]; then
    green=$(tput setaf 2); red=$(tput setaf 1)
    blue=$(tput setaf 4); reset=$(tput sgr0)
else
    green=""; red=""; blue=""; reset=""
fi
```

---

## gpg-setup-secure.sh

One-time setup script for a new build instance. Run it once; then follow
the printed instructions to obtain your key's keygrip.

It writes `~/.gnupg/gpg-agent.conf` with a 24-hour passphrase cache and
`allow-preset-passphrase`, restarts `gpg-agent`, then prints the
`gpg-preset-passphrase` command you need to run with your keygrip. Find
your keygrip with:

```bash
gpg --with-keygrip -K
```

---

## gpg-bashrc.sh

Add the contents to `~/.bashrc` or `~/.pgsql_profile`. On login it tests
whether a GPG signing operation succeeds; if not it calls
`preset_gpg_passphrase` from `global.sh` to pre-load the passphrase into
the running agent.

Before deploying, replace the placeholder keygrip:

```bash
export GPG_KEYGRIP="XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
```

Also ensure `GPG_KEY_ID` is set in `global.sh`, as it is referenced by the
test signing call in this file.

---

## packagebuild.sh

Builds packages from the git tree and signs the resulting RPMs. The script
automatically detects whether a package lives in the common, non-common, or
extras repository and acts accordingly.

### Usage

```
packagebuild.sh [--beta] [--testing] <git-package-name> <sign-package-name> [pg-version]
```

- `--beta` — build against the current beta PostgreSQL version
  (`pgBetaVersion` in `global.sh`). Exits with an error if
  `pgBetaVersion` is unset.
- `--testing` — build against `pgTestBuilds` versions and target testing
  repository targets.
- `<git-package-name>` — the directory name in the git tree (e.g.
  `postgresql-16`, `pgpool-II-41`).
- `<sign-package-name>` — the prefix used by `rpmsign` to locate built
  RPMs (e.g. `postgresql16`, `pgpool-II`). These differ because upstream
  names don't always match packaging conventions (e.g. `check_pgactivity`
  is packaged as `nagios-check_pgactivity`).
- `[pg-version]` — optional; restricts the build to a single PostgreSQL
  major version. If omitted, all versions in the active build array are
  built.

### Build logic

The script checks three locations in order and stops at the first match:

1. **Common** (`~/git/pgrpms/rpm/redhat/main/common/<pkg>/<git_os>`) —
   builds once with `make commonbuild` (or `commonbuildtesting`), signs
   against `rpmcommon`, and exits.
2. **Non-common** (`~/git/pgrpms/rpm/redhat/main/non-common/<pkg>/<git_os>`) —
   iterates over every version in `pgStableBuilds` (or `pgTestBuilds`),
   runs `make build<version>` (or `build<version>testing`), and signs
   each version's directory separately.
3. **Extras** (`~/git/pgrpms/rpm/redhat/main/extras/<pkg>/<git_os>`) —
   builds once with `make extrasbuild` (or `extrasbuildtesting`), signs
   against `pgdg`, and exits. Only available when `extrasrepoenabled=1`.

On any build failure, a timestamped log is written to `~/bin/logs/` and
the script exits immediately.

---

## packagebuildnonfree.sh

Identical in structure to `packagebuild.sh` but operates exclusively on
the `non-free` directory in the git tree. Kept as a separate script
deliberately, to prevent accidentally building proprietary packages on
shared community build instances. It does not support `--beta` or
`--testing` flags and has no extras/common handling.

---

## packagesync.sh

Publishes built RPMs to the production (or testing) repository. This is the
most capable script in the collection. It must be called with explicit sync
targets; running it without arguments prints the usage message.

### Usage

```
packagesync.sh [--testing] --sync=<target>
```

Multiple space-separated targets can be combined inside a single `--sync`
value:

```bash
packagesync.sh --sync=all                    # common + extras + all stable versions
packagesync.sh --sync=common                 # only the common repo
packagesync.sh --sync=extras                 # only the extras repo
packagesync.sh --sync=pg                     # all stable PostgreSQL versions
packagesync.sh --sync=18                     # a single version
packagesync.sh --sync=alpha                  # alpha build (pgAlphaVersion)
packagesync.sh --sync=beta                   # beta build (pgBetaVersion)
packagesync.sh --sync="18 common"            # version 18 plus common
packagesync.sh --sync="alpha common"
packagesync.sh --sync="pg common extras"
packagesync.sh --testing --sync=18           # version 18 in testing repos
packagesync.sh --testing --sync=pg           # all versions in testing repos
```

### What each sync does

For every target, the script:

1. Consolidates arch-specific and noarch RPMs into an `ALLRPMS` staging
   directory using `rsync --checksum --delete`.
2. Separates debuginfo/debugsource packages into `ALLDEBUGRPMS`.
3. Consolidates SRPMs into `ALLSRPMS`.
4. Runs `createrepo` with `--changelog-limit=3 --workers=4` and the
   appropriate comps group XML file (for versioned repos).
5. Signs each `repomd.xml` with `gpg2 --pinentry-mode loopback`.
6. Syncs packages and repodata separately to S3 (packages without
   `--delete`, repodata with `--delete` to remove stale metadata).
7. Creates CloudFront invalidations for the repodata paths.

When `osislatest=1`, steps 6–7 are repeated for the major-version path
(e.g. `rhel-10-x86_64`) in addition to the full minor-version path
(`rhel-10.1-x86_64`), because S3 has no symlink support.

SLES and openSUSE Leap builds use the `zypp/zypp` sync base and `zypp-*` S3 buckets; all
other distros use `yum/yum` and `dnf-*` buckets. This is determined
automatically from `osdistro` in `global.sh` — both `suse` and `opensuse`
map to the zypp path.

Testing mode (`--testing`) routes syncs to `testing/` prefixed S3 paths
and uses `pgTestBuilds` rather than `pgStableBuilds`. The `sync_extras`
function skips testing mode entirely (extras have no testing repo).

---

## packagesyncnonfree.sh

Equivalent of `packagesync.sh` for non-free packages. Key differences:

- Reads `pgStableBuilds` only; no testing mode, no extras, no common.
- Copies packages from `rpmcommon` into each version directory first
  (non-free has no common repo, so common packages are duplicated).
- Syncs to an `non-free/<version>/...` S3 path.
- Uses stricter error handling (`set -euo pipefail`) and validates
  prerequisites (AWS CLI, credentials, `rsync`, `createrepo`, `gpg2`)
  before starting.
- Accepts an optional positional argument to restrict sync to a single
  PostgreSQL version.

---

## dailybuildalpha.sh

Automated daily build script for the current alpha/development PostgreSQL
version (`pgAlphaVersion`). Intended to be run from cron.

### Usage

```
dailybuildalpha.sh [--verbose] [--skip-cleanup] [--skip-sync]
```

### Build sequence

1. **Prerequisite check** — verifies the git repo directory exists,
   `packagesync.sh` is present, and `gpg-agent` is running.
2. **Prepare environment** — `cd` into the git directory and run
   `git clean -dfx` for a clean build state.
3. **Prepare source** — `make prep<pgAlphaVersion>` downloads and
   patches the PostgreSQL source tarball.
4. **Build packages** — `make noprepbuild<pgAlphaVersion>testing` compiles
   and produces RPMs.
5. **Clean old packages** — deletes files older than 1 day from all
   `rpm<pgAlphaVersion>testing*/` directories and removes stale `.sig`
   files. Skip with `--skip-cleanup`.
6. **Sign packages** — calls `sign_package` from `global.sh` against the
   alpha testing directory.
7. **Sync packages** — calls `packagesync.sh --sync=alpha`. Skip with
   `--skip-sync`.

Errors at any step (except sync warnings) abort the script immediately
(`set -e`). Execution time is logged at the end.

---

## cleanbuilddirs.sh

Removes `BUILD/` and `BUILDROOT/` directories left behind by failed
`rpmbuild` runs. Under normal circumstances `rpmbuild` cleans these itself,
but failures leave them populated, causing subsequent builds to fail or
pick up stale files.

Cleans the following directories:

- `~/rpmcommon/` — common package build tree
- `~/rpm<pgAlphaVersion>testing/` — current alpha build tree
- `~/rpm<version>testing/` for all versions in `pgTestBuilds`
- `~/pgdg.extras/` — extras build tree (when `extrasrepoenabled=1`)
- `~/rpm<version>/` for all versions in `pgStableBuilds`

Run this only when no builds are in progress to avoid disrupting active
compilation.

---

## check_upload_status.sh

Validates that published repositories are accessible at
`download.postgresql.org`. For each version in `pgStableBuilds` and for
the `common` repo it fetches the `repodata/` URL with `curl` and checks
for an HTTP 404, printing a coloured error if the repository is missing.

Useful to run immediately after a sync to confirm everything published
successfully.

---

## awsupdateindex.sh

Regenerates the `index.html` files on the SRPM and debuginfo S3 buckets
using [s3indexbuilder.py](https://github.com/mhagander/s3indexbuilder).
S3 does not serve directory listings natively, so this script creates HTML
index pages to allow browsing.

After building the indexes it creates CloudFront invalidations for the
`/srpms` and `/debug` paths.

Run this on one RHEL/Fedora instance (for `dnf-*` buckets) and separately
on one SLES instance (for `zypp-*` buckets). Requires Python ≥ 3.10.
Add to cron at 4 AM, or run manually after `packagesync.sh`.

---

## postgresqldbserver-16.xml

A comps group definition file consumed by `createrepo -g` to define
package groups within the repository (e.g. "PostgreSQL Database Server").
`packagesync.sh` and `packagesyncnonfree.sh` reference these files from
`/usr/local/etc/postgresqldbserver-<version>.xml`.

A copy is required for each supported major PostgreSQL version. The file
should eventually be co-located with the scripts rather than kept in
`/usr/local/etc`.

---

## Typical Workflows

### Initial instance setup

```bash
# 1. Configure global.sh with correct OS, arch, AWS, and GPG values.
# 2. Set up GPG agent:
bash ~/bin/gpg-setup-secure.sh
gpg --with-keygrip -K         # Note the keygrip
# 3. Add gpg-bashrc.sh to ~/.bashrc and set GPG_KEYGRIP
# 4. Re-login or source ~/.bashrc
```

### Build and publish a single package

```bash
# Build postgis34 for all stable versions:
~/bin/packagebuild.sh postgis34 postgis34

# Build only against PostgreSQL 17:
~/bin/packagebuild.sh postgis34 postgis34 17

# Sync version 17 to production:
~/bin/packagesync.sh --sync=17
```

### Publish a new common package

```bash
~/bin/packagebuild.sh pg_activity pg_activity
~/bin/packagesync.sh --sync=common
```

### Daily alpha cron entry

```
TERM=xterm
0 2 * * * /var/lib/pgsql/bin/dailybuildalpha.sh >> /var/log/pgbuild-alpha.log 2>&1
```

### Post-sync validation

```bash
~/bin/check_upload_status.sh
```

### Update S3 index pages

```bash
~/bin/awsupdateindex.sh
```

---

## Dependencies

| Tool | Purpose |
|---|---|
| `rpmbuild` / `rpmsign` | Building and signing RPM packages |
| `gpg2` / `gpg-agent` | Package and repodata signing |
| `/usr/libexec/gpg-preset-passphrase` | Pre-loading passphrase into agent cache |
| `createrepo` | Generating repository metadata |
| `rsync` | Staging RPMs into sync directories |
| `aws` (CLI) | S3 sync and CloudFront invalidation |
| `curl` | Repository availability checks in `check_upload_status.sh` |
| `s3indexbuilder.py` | HTML index generation for S3 (requires Python ≥ 3.10) |
| `git` | Source checkout and workspace cleaning in `dailybuildalpha.sh` |
