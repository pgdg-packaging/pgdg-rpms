%global sname pg_parquet
# cargo-pgrx has to be the same version as the pgrx crate that the extension
# uses. Upstream pins pgrx 0.19.3, we build with 0.19.5, see %%prep:
%global pgrx_series 0.19
%global pgrx_version 0.19.5

Summary:	Copy data between PostgreSQL and Parquet files
Name:		%{sname}_%{pgmajorversion}
Version:	0.6.1
Release:	1PGDG%{?dist}
%if 0%{?pgminorversion:1}
# pgminorversion is the PostgreSQL minor release that the build servers
# build against (global/Makefile.global): require at least that one, at
# build time and at runtime.
# The other postgresqlNN-* dependencies need no version here: the PostgreSQL
# subpackages require each other's exact version-release (all of them pin
# the client package, which pins -libs), so the server, contrib etc. follow
# -devel at build time and -libs at runtime.
BuildRequires:	postgresql%{pgmajorversion}-devel >= %{pgminorversion}
Requires:	postgresql%{pgmajorversion}-libs%{?_isa} >= %{pgminorversion}
%endif
# The extension itself, and the licenses of the Rust crates that are compiled into
# it (353 crates), checked with "cargo metadata --filter-platform
# x86_64-unknown-linux-gnu", without the dev dependencies:
License:	PostgreSQL AND MIT AND Apache-2.0 AND Unicode-3.0 AND ISC AND BSD-3-Clause AND BSD-2-Clause AND Zlib AND CC0-1.0
URL:		https://github.com/CrunchyData/%{sname}
Source0:	https://github.com/CrunchyData/%{sname}/archive/refs/tags/v%{version}.tar.gz#/%{sname}-%{version}.tar.gz
# Cargo.lock and the dependencies of the crate, for building without network
# access. Made with "./pg_parquet-vendor.sh %%{version}", which updates pgrx to
# %%{pgrx_version} in Cargo.lock, and runs cargo-vendor-filterer for the Linux
# architectures that we build on.
# It has to be made again for every new version, and for every new
# cargo-pgrx019 release.
Source1:	https://download.postgresql.org/pub/repos/yum/rust-sources/%{sname}/%{sname}-%{version}-vendor.tar.xz

# pgrx 0.19 and edition 2024 need Rust 1.96:
BuildRequires:	rust >= 1.96
BuildRequires:	cargo >= 1.96
# pgrx-pg-sys runs rustfmt on the generated bindings (a separate package on
# Fedora, RHEL and Amazon Linux, part of the rust package on SLES):
%if 0%{?rhel} || 0%{?fedora} || 0%{?amzn}
BuildRequires:	rustfmt
%endif
%if 0%{?suse_version} >= 1600
BuildRequires:	rust1.98
%endif
BuildRequires:	cargo-pgrx019 = %{pgrx_version}
BuildRequires:	postgresql%{pgmajorversion}-devel
# "cargo pgrx init" in %%build runs initdb:
BuildRequires:	postgresql%{pgmajorversion}-server
# pgrx-pg-sys generates the bindings of the PostgreSQL headers with bindgen:
%if 0%{?suse_version} == 1600
BuildRequires:	llvm19-devel clang19-devel
%endif
%if 0%{?amzn}
BuildRequires:	llvm-devel >= 15.0 clang-devel >= 15.0
%endif
%if ( 0%{?fedora} || 0%{?rhel} ) && !0%{?amzn}
BuildRequires:	llvm-devel >= 19.0 clang-devel >= 19.0
%endif

# Native code of the crates (aws-lc-sys, ring, zstd-sys, lz4-sys):
BuildRequires:	gcc gcc-c++ make cmake
Requires:	postgresql%{pgmajorversion}-server

%description
pg_parquet is a PostgreSQL extension that allows you to read and write Parquet
files, which are located in S3, Azure Blob Storage, Google Cloud Storage,
http(s) endpoints or the file system, from PostgreSQL via COPY TO/FROM
commands. It depends on the Apache Arrow project to read and write Parquet
files.

%prep
%setup -q -n %{sname}-%{version} -a 1

# Some vendored sources are executable, and their "#![...]" first line ends up
# in the debugsource package, where brp-mangle-shebangs takes it as a shebang
# and fails:
find vendor -name '*.rs' -perm /111 -exec chmod a-x {} +

# Build with the pgrx version of our cargo-pgrx package. Cargo.lock of the
# vendor tarball already has it:
sed -i -E 's/^(pgrx(-tests)? = )"=[0-9.]+"/\1"=%{pgrx_version}"/' Cargo.toml

# Use the vendored crates, and nothing from the network:
cat >> .cargo/config.toml <<'CARGOEOF'

[source.crates-io]
replace-with = "vendored-sources"

[source.vendored-sources]
directory = "vendor"
CARGOEOF

%build
export CARGO_HOME="$PWD/.cargo-home"
export PGRX_HOME="$PWD/.pgrx-home"
# Keep the debug information for the debuginfo package:
export CARGO_PROFILE_RELEASE_DEBUG=2
export CARGO_PROFILE_RELEASE_STRIP=none
export RUSTFLAGS="%{?build_rustflags}"
export PATH=%{pginstdir}/bin:$PATH
# ccache 3.7 on RHEL 8 fails on the assembler files of aws-lc-sys with
# "Internal error in format":
export CCACHE_DISABLE=1

# Point pgrx to the installed PostgreSQL. This writes $PGRX_HOME/config.toml
# and does not download or build a PostgreSQL:
cargo-pgrx-%{pgrx_series} pgrx init --pg%{pgmajorversion}=%{pginstdir}/bin/pg_config

# The default feature is pg19, so select the feature of our PostgreSQL version:
cargo-pgrx-%{pgrx_series} pgrx package --pg-config %{pginstdir}/bin/pg_config \
	--no-default-features --features pg%{pgmajorversion}

%install
mkdir -p %{buildroot}
cp -a target/release/%{sname}-pg%{pgmajorversion}/* %{buildroot}/

%files
%license LICENSE
%doc README.md
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}.control
%{pginstdir}/share/extension/%{sname}--*.sql

%changelog
* Sun Nov 22 2026 Devrim Gunduz <devrim@gunduz.org> - 0.6.1-1PGDG
- Update to 0.6.1 per changes described at:
  https://github.com/CrunchyData/pg_parquet/releases/tag/v0.6.0
  https://github.com/CrunchyData/pg_parquet/compare/v0.6.0...v0.6.1
- Build with pgrx 0.19.5 and cargo-pgrx019, as upstream moved to pgrx 0.19.
  pgrx 0.19 uses bindgen 0.72 itself, so remove the bindgen update in %%prep.
- Add PostgreSQL 19 support.
- No more builds for RHEL 8 and SLES 15: cargo-pgrx019 is not available
  there. 0.5.1 stays in those repositories.
- Add postgresqlNN-server BR: "cargo pgrx init" of pgrx 0.19 runs initdb.
- Update License: tag for the new set of crates.

* Tue Nov 10 2026 Devrim Gündüz <devrim@gunduz.org> - 0.5.1-3PGDG
- Use a new vendor tarball with the real prettyplease crate instead of an
  empty stub. On ppc64le aws-lc-sys builds bindgen with its default
  features, which need prettyplease, so the build failed there.

* Mon Nov 9 2026 Devrim Gündüz <devrim@gunduz.org> - 0.5.1-2PGDG
- Rebuild against latest PostgreSQL minor releases
- Require at least the PostgreSQL minor release that the package is
  built against (pgminorversion, set by the build server Makefiles).

* Mon Oct 5 2026 Devrim Gündüz <devrim@gunduz.org> - 0.5.1-1PGDG
- Initial packaging for the PostgreSQL RPM repository.
