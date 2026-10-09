%global sname pgvectorscale
%global pname vectorscale
# cargo-pgrx has to be the same version as the pgrx crate that the extension uses:
%global pgrx_series 0.16

Summary:	Faster and cheaper vector search on PostgreSQL, complementing pgvector
Name:		%{sname}_%{pgmajorversion}
Version:	0.9.1
Release:	1PGDG%{?dist}
# The extension itself, and the licenses of the Rust crates that are compiled into
# it (161 crates), checked with "cargo metadata --filter-platform
# x86_64-unknown-linux-gnu", without the dev dependencies:
License:	PostgreSQL AND MIT AND Apache-2.0 AND Unicode-3.0 AND ISC AND Zlib AND BSD-3-Clause
URL:		https://github.com/timescale/%{sname}
Source0:	https://github.com/timescale/%{sname}/archive/refs/tags/%{version}.tar.gz#/%{sname}-%{version}.tar.gz
# Cargo.lock and the dependencies of the crate, for building without network
# access. Upstream does not ship a Cargo.lock. Made with
# "./pgvectorscale-vendor.sh %%{version}", which creates Cargo.lock and runs
# cargo-vendor-filterer for the Linux architectures that we build on. It also
# vendors bindgen 0.72.1, see %%prep.
# It has to be made again for every new version.
# The CDN cached a 404 for the plain URL. The query string makes it fetch
# the file again; #/ keeps the local file name unchanged.
Source1:	https://download.postgresql.org/pub/repos/yum/rust-sources/%{sname}/%{sname}-%{version}-vendor.tar.xz?v=2#/%{sname}-%{version}-vendor.tar.xz

# The newest crates in Cargo.lock need Rust 1.88:
BuildRequires:	rust >= 1.88
BuildRequires:	cargo >= 1.88
# pgrx-pg-sys runs rustfmt on the generated bindings (a separate package on
# Fedora, RHEL and Amazon Linux, part of the rust package on SLES):
%if 0%{?rhel} || 0%{?fedora} || 0%{?amzn}
BuildRequires:	rustfmt
%endif
%if 0%{?suse_version} >= 1600
BuildRequires:	rust1.98
%endif
BuildRequires:	cargo-pgrx016 = 0.16.1
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

BuildRequires:	gcc
Requires:	postgresql%{pgmajorversion}-server
# The extension needs the vector extension:
Requires:	pgvector_%{pgmajorversion}

%description
pgvectorscale complements pgvector, the open-source vector data extension for
PostgreSQL, and introduces the following key innovations for pgvector data:

* A new index type called StreamingDiskANN, inspired by the DiskANN algorithm,
  based on research from Microsoft.
* Statistical Binary Quantization: developed by Timescale researchers, this
  compression method improves on standard Binary Quantization.
* Label-based filtered vector search: based on Microsoft's Filtered DiskANN
  research, this allows you to combine vector similarity search with label
  filtering for more precise and efficient results.

On x86_64, pgvectorscale needs a CPU with AVX2 and FMA support.

%prep
%setup -q -n %{sname}-%{version} -a 1

# Use the vendored crates, and nothing from the network. Upstream's
# .cargo/config.toml only sets the rustflags, which are set below:
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
# RUSTFLAGS overrides the rustflags of .cargo/config.toml. The distance
# functions are written for AVX2 and FMA on x86_64, and the build fails without
# them. The extension checks the CPU when it is loaded:
RUSTFLAGS="%{?build_rustflags}"
%ifarch x86_64
RUSTFLAGS="$RUSTFLAGS -Ctarget-feature=+avx2,+fma"
%endif
export RUSTFLAGS
export PATH=%{pginstdir}/bin:$PATH

# Point pgrx to the installed PostgreSQL. This writes $PGRX_HOME/config.toml
# and does not download or build a PostgreSQL:
cargo-pgrx-%{pgrx_series} pgrx init --pg%{pgmajorversion}=%{pginstdir}/bin/pg_config

# It builds with the features of the PostgreSQL version of pg_config:
cd %{sname}
cargo-pgrx-%{pgrx_series} pgrx package --pg-config %{pginstdir}/bin/pg_config

%install
mkdir -p %{buildroot}
cp -a target/release/%{pname}-pg%{pgmajorversion}/* %{buildroot}/

%files
%license LICENSE NOTICE
%doc README.md
%{pginstdir}/lib/%{pname}*.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}--*.sql

%changelog
* Fri Sep 25 2026 Devrim Gündüz <devrim@gunduz.org> - 0.9.1-1PGDG
- Initial packaging for the PostgreSQL RPM repository.
