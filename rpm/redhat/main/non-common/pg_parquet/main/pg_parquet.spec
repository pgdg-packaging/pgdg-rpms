%global sname pg_parquet
# cargo-pgrx has to be the same version as the pgrx crate that the extension
# uses. Upstream pins pgrx 0.16.0, we build with 0.16.1, see %%prep:
%global pgrx_series 0.16
%global pgrx_version 0.16.1

Summary:	Copy data between PostgreSQL and Parquet files
Name:		%{sname}_%{pgmajorversion}
Version:	0.5.1
Release:	1PGDG%{?dist}
# The extension itself, and the licenses of the Rust crates that are compiled into
# it (334 crates), checked with "cargo metadata --filter-platform
# x86_64-unknown-linux-gnu", without the dev dependencies:
License:	PostgreSQL AND MIT AND Apache-2.0 AND Unicode-3.0 AND ISC AND OpenSSL AND BSD-3-Clause AND Zlib AND CC0-1.0
URL:		https://github.com/CrunchyData/%{sname}
Source0:	https://github.com/CrunchyData/%{sname}/archive/refs/tags/v%{version}.tar.gz#/%{sname}-%{version}.tar.gz
# Cargo.lock and the dependencies of the crate, for building without network
# access. Made with "./pg_parquet-vendor.sh %%{version}", which updates pgrx to
# %%{pgrx_version} in Cargo.lock, and runs cargo-vendor-filterer for the Linux
# architectures that we build on.
# It has to be made again for every new version.
Source1:	https://download.postgresql.org/pub/repos/yum/rust-sources/%{sname}/%{sname}-%{version}-vendor.tar.xz

# The newest crates in Cargo.lock need Rust 1.86:
BuildRequires:	rust >= 1.86
BuildRequires:	cargo >= 1.86
# pgrx-pg-sys runs rustfmt on the generated bindings (a separate package on
# Fedora, RHEL and Amazon Linux, part of the rust package on SLES):
%if 0%{?rhel} || 0%{?fedora} || 0%{?amzn}
BuildRequires:	rustfmt
%endif
%if 0%{?suse_version} >= 1600
BuildRequires:	rust1.98
%endif
BuildRequires:	cargo-pgrx016 = %{pgrx_version}
BuildRequires:	postgresql%{pgmajorversion}-devel
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

# pgrx-bindgen 0.16.1 needs bindgen 0.71, which creates opaque structs from the
# PostgreSQL headers with newer clang versions (seen with clang 22 on Fedora 44),
# and the build then fails. Use bindgen 0.72.1 instead, as pgrx 0.17 does. It
# is in the vendor tarball too:
sed -i '/^\[dependencies.bindgen\]$/{n;s/^version = "0.71.1"$/version = "0.72.1"/}' vendor/pgrx-bindgen/Cargo.toml
sed -i 's/"Cargo.toml":"[0-9a-f]*",//' vendor/pgrx-bindgen/.cargo-checksum.json
CARGO_HOME="$PWD/.cargo-home" cargo update --offline -p bindgen@0.71.1 --precise 0.72.1

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

# The default feature is pg18, so select the feature of our PostgreSQL version:
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
* Mon Oct 5 2026 Devrim Gündüz <devrim@gunduz.org> - 0.5.1-1PGDG
- Initial packaging for the PostgreSQL RPM repository.
