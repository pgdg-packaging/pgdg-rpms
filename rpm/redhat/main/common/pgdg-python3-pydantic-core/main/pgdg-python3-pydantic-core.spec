%pgdg_python3_setup

%global	modname pydantic-core
%global	pymodname pydantic_core

Name:		python%{python3_pkgversion}-%{modname}
# RHEL 10 gets pydantic 2.9.2, which needs exactly 2.23.4 (see the
# pydantic spec file):
%if 0%{?rhel} == 10
Version:	2.23.4
%else
Version:	2.33.2
%endif
Release:	43PGDG%{?dist}
Summary:	Core validation logic for pydantic written in Rust
# pydantic-core is MIT. The licenses of the crates that are compiled into the
# extension, checked with "cargo tree -e normal" (87 crates for 2.33.2; 2.23.4
# on RHEL 10 adds the last two):
%if 0%{?rhel} == 10
License:	MIT AND (MIT OR Apache-2.0) AND (Apache-2.0 OR BSL-1.0) AND (BSD-2-Clause OR Apache-2.0 OR MIT) AND Apache-2.0 WITH LLVM-exception AND Unicode-3.0 AND Unicode-DFS-2016 AND (Unlicense OR MIT) AND (Zlib OR Apache-2.0 OR MIT)
%else
License:	MIT AND (MIT OR Apache-2.0) AND (Apache-2.0 OR BSL-1.0) AND (BSD-2-Clause OR Apache-2.0 OR MIT) AND Apache-2.0 WITH LLVM-exception AND Unicode-3.0 AND Unicode-DFS-2016
%endif
URL:		https://github.com/pydantic/%{modname}
Source0:	https://files.pythonhosted.org/packages/source/p/%{pymodname}/%{pymodname}-%{version}.tar.gz
# The crates that pydantic-core depends on, for building without network
# access. Made with "./pgdg-python3-pydantic-core-vendor.sh %%{version}", which
# runs cargo-vendor-filterer for the Linux architectures that we build on.
# It has to be made again for every new version.
# The CDN cached a 404 for the plain URL. The query string makes it fetch
# the file again; #/ keeps the local file name unchanged.
Source1:	https://download.postgresql.org/pub/repos/yum/rust-sources/%{modname}/%{pymodname}-%{version}-vendor.tar.xz?v=3#/%{pymodname}-%{version}-vendor.tar.xz

BuildRequires:	python%{python3_pkgversion}-devel
BuildRequires:	python%{python3_pkgversion}-pip
BuildRequires:	python%{python3_pkgversion}-maturin >= 1
BuildRequires:	python%{python3_pkgversion}-typing-extensions
BuildRequires:	pyproject-rpm-macros
# rust-version in Cargo.toml of this release:
BuildRequires:	rust >= 1.75
BuildRequires:	cargo >= 1.75
BuildRequires:	gcc

Requires:	python%{python3_pkgversion}-typing-extensions >= 4.6.0
%if 0%{?rhel} == 10
# Replace the EPEL package of the same module, which has the same files:
Obsoletes:	python3-%{modname} < %{version}-%{release}
%endif

%description
pydantic-core provides the core validation and serialization functionality
of pydantic, written in Rust. Every pydantic release needs exactly one
pydantic-core release; this one is for pydantic 2.11 (2.9 on RHEL 10).

%prep
%setup -q -n %{pymodname}-%{version} -a 1

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
# Keep the debug information for the debuginfo package:
export CARGO_PROFILE_RELEASE_DEBUG=2
export CARGO_PROFILE_RELEASE_STRIP=none
%{?build_rustflags:export RUSTFLAGS="%{build_rustflags}"}
# Make maturin run cargo with the locked, vendored crates only:
export MATURIN_PEP517_ARGS="--frozen"
%pyproject_wheel

%install
%pyproject_install

%files
%license LICENSE
%doc README.md
%{python3_sitearch}/%{pymodname}/
%{python3_sitearch}/%{pymodname}-%{version}.dist-info/

%changelog
* Wed Oct 28 2026 Devrim Gunduz <devrim@gunduz.org> - 2.33.2-43PGDG
- Use %%pgdg_python3_setup from pgdg-srpm-macros 2.5.0 instead of the
  per-distro Python block and the __ospython macro. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/462

* Sat Oct 24 2026 Devrim Gunduz <devrim@gunduz.org> - 2.33.2-42PGDG
- Add RHEL 10 support, without EPEL: use 2.23.4 there, for pydantic 2.9.2,
  with its own vendored crates tarball, and obsolete the EPEL
  python3-pydantic-core package. Start the release from 42, so that our
  packages win over EPEL's. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/422

* Wed Oct 07 2026 Devrim Gunduz <devrim@gunduz.org> - 2.33.2-1PGDG
- Initial packaging for the PostgreSQL RPM repository, to satisfy pydantic
  dependency (for pg_statviz) on Amazon Linux 2023. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/249
- Add RHEL 9 support (python3.12), for pg_statviz. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/249
