%global sname postgresql_anonymizer
# cargo-pgrx has to be the same version as the pgrx crate that the extension uses:
%global pgrx_series 0.19

Summary:	Anonymization & Data Masking for PostgreSQL
Name:		%{sname}_%{pgmajorversion}
Version:	3.2.2
Release:	1PGDG%{?dist}
# The extension itself, and the licenses of the Rust crates that are compiled into
# it (236 crates), checked with "cargo metadata --filter-platform
# x86_64-unknown-linux-gnu", without the dev dependencies:
License:	PostgreSQL AND MIT AND Apache-2.0 AND BSD-2-Clause AND BSD-3-Clause AND Unicode-3.0 AND ISC AND Zlib AND 0BSD AND Unlicense AND CC0-1.0
URL:		https://labs.dalibo.com/postgresql_anonymizer
Source0:	https://gitlab.com/dalibo/%{sname}/-/archive/%{version}/%{sname}-%{version}.tar.gz
# The dependencies of the crate, for building without network access. Made with:
#   tar xf postgresql_anonymizer-%%{version}.tar.gz && cd postgresql_anonymizer-%%{version}
#   cargo vendor vendor
#   tar --sort=name --mtime=@0 --owner=0 --group=0 --numeric-owner -cf - vendor | xz -T0 -6 > ../postgresql_anonymizer-%%{version}-vendor.tar.xz
# It is not "cargo vendor --locked", as Cargo.lock of upstream has the wrong version
# of the crate itself. It has to be made again for every new version.
Source1:	https://download.postgresql.org/pub/repos/yum/rust-sources/%{sname}-%{version}-vendor.tar.xz

# pgrx 0.19 and edition 2024 need Rust 1.96:
BuildRequires:	rust >= 1.96
BuildRequires:	cargo >= 1.96
# pgrx-pg-sys runs rustfmt on the generated bindings (a separate package on
# Fedora and Amazon Linux, part of the rust package on SLES):
%if 0%{?rhel} || 0%{?fedora} || 0%{?amzn}
BuildRequires:	rustfmt
%endif
%if 0%{?suse_version} >= 1600
BuildRequires:	rust1.98
%endif
BuildRequires:	cargo-pgrx019 = 0.19.1
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

%description
PostgreSQL Anonymizer is an extension to mask or replace personally identifiable
information (PII) or commercially sensitive data from a PostgreSQL database.

The project has a declarative approach of anonymization. This means you can
declare the masking rules using the PostgreSQL Data Definition Language (DDL)
and specify your anonymization strategy inside the table definition itself.

This is the Rust version of the extension (3.x). It is not compatible with the
old 1.x versions that were built with C: the extension has to be created again
in the databases that used them.

%prep
%setup -q -n %{sname}-%{version} -a 1

# Cargo.lock of this release still has the version of the development branch:
sed -i '/^name = "anon"$/{n;s/^version = .*/version = "%{version}"/}' Cargo.lock

# Use the vendored crates, and nothing from the network:
mkdir -p .cargo
cat > .cargo/config.toml <<'CARGOEOF'
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
%{?build_rustflags:export RUSTFLAGS="%{build_rustflags}"}
export PATH=%{pginstdir}/bin:$PATH

# Point pgrx to the installed PostgreSQL. This writes $PGRX_HOME/config.toml
# and does not download or build a PostgreSQL:
cargo-pgrx-%{pgrx_series} pgrx init --pg%{pgmajorversion}=%{pginstdir}/bin/pg_config

# It builds with the features of the PostgreSQL version of pg_config:
cargo-pgrx-%{pgrx_series} pgrx package --pg-config %{pginstdir}/bin/pg_config

%install
mkdir -p %{buildroot}
cp -a target/release/anon-pg%{pgmajorversion}/* %{buildroot}/

# The data files, as in the Makefile of upstream:
install -d %{buildroot}%{pginstdir}/share/extension/anon
install -pm 0644 data/*.csv data/en_US/fake/*.csv %{buildroot}%{pginstdir}/share/extension/anon/

%files
%license LICENSE.md
%doc README.md NEWS.md CHANGELOG.md AUTHORS.md
%{pginstdir}/lib/anon.so
%{pginstdir}/share/extension/anon.control
%{pginstdir}/share/extension/anon--*.sql
%{pginstdir}/share/extension/anon/

%changelog
* Mon Sep 21 2026 Devrim Gündüz <devrim@gunduz.org> - 3.2.2-1PGDG
- Initial packaging of the Rust version of PostgreSQL Anonymizer for the
  PostgreSQL RPM repository. The C versions (1.x) were removed from the
  repository earlier. This is the first Rust package of the repository.
