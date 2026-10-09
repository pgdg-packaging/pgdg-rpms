%if 0%{?fedora} && 0%{?fedora} == 45
%global __ospython %{_bindir}/python3.15
%global python3_pkgversion 3.15
%endif
%if 0%{?fedora} && 0%{?fedora} <= 44
%global __ospython %{_bindir}/python3.14
%global python3_pkgversion 3.14
%endif
%if 0%{?rhel} && 0%{?rhel} <= 10
%global	__ospython %{_bindir}/python3.12
%global	python3_pkgversion 3.12
%endif
%if 0%{?rhel} == 9
%global	__python3 %{_bindir}/python3.12
%endif
%if 0%{?amzn} == 2023
%global	__ospython %{_bindir}/python3.13
%global	__python3 %{_bindir}/python3.13
%global	python3_pkgversion 3.13
%endif
%if 0%{?suse_version} == 1500
%global	__ospython %{_bindir}/python3.11
%global	python3_pkgversion 311
%endif
%if 0%{?suse_version} == 1600
%global	__ospython %{_bindir}/python3.13
%global	python3_pkgversion 313
%endif

%global	modname jiter

Name:		python%{python3_pkgversion}-%{modname}
Version:	0.17.0
Release:	1PGDG%{?dist}
Summary:	Fast iterable JSON parser
# jiter is MIT. The licenses of the crates that are compiled into the
# extension, checked with "cargo tree -p jiter-python -e normal" (40 crates):
License:	MIT AND (MIT OR Apache-2.0) AND (BSD-2-Clause OR Apache-2.0 OR MIT) AND Unicode-3.0
URL:		https://github.com/pydantic/%{modname}
Source0:	https://files.pythonhosted.org/packages/source/j/%{modname}/%{modname}-%{version}.tar.gz
# The crates that jiter depends on, for building without network access. Made
# with "./pgdg-python3-jiter-vendor.sh %%{version}", which runs
# cargo-vendor-filterer for the Linux architectures that we build on.
# It has to be made again for every new version.
# The CDN cached a 404 for the plain URL. The query string makes it fetch
# the file again; #/ keeps the local file name unchanged.
Source1:	https://download.postgresql.org/pub/repos/yum/rust-sources/%{modname}/%{modname}-%{version}-vendor.tar.xz?v=2#/%{modname}-%{version}-vendor.tar.xz

BuildRequires:	python%{python3_pkgversion}-devel
BuildRequires:	python%{python3_pkgversion}-pip
%if 0%{?suse_version}
BuildRequires:	python-rpm-macros
%else
BuildRequires:	pyproject-rpm-macros
%endif
%if 0%{?amzn} == 2023 || 0%{?rhel} == 9
BuildRequires:	python%{python3_pkgversion}-maturin >= 1.15.0
%endif
%if 0%{?suse_version}
# SLES 16 has maturin 1.8.7, which builds this release too:
BuildRequires:	python%{python3_pkgversion}-maturin
%endif
%if 0%{?rhel} == 10
# EPEL 10 has maturin 1.9.6. pyproject.toml asks for 1.15.0, but pip does
# not check the build requirements with --no-build-isolation, and older
# releases build this release fine:
BuildRequires:	maturin
%endif
%if 0%{?fedora}
BuildRequires:	maturin >= 1.15.0
%endif
# rust-version in Cargo.toml of this release:
BuildRequires:	rust >= 1.88
BuildRequires:	cargo >= 1.88
BuildRequires:	gcc

%description
jiter is a fast iterable JSON parser, written in Rust, with Python bindings.
It is used by the anthropic and openai Python SDKs to parse partial JSON
while streaming.

%prep
%setup -q -n %{modname}-%{version} -a 1

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
%{python3_sitearch}/%{modname}/
%{python3_sitearch}/%{modname}-%{version}.dist-info/

%changelog
* Wed Oct 07 2026 Devrim Gunduz <devrim@gunduz.org> - 0.17.0-1PGDG
- Initial packaging for the PostgreSQL RPM repository, to satisfy
  anthropic dependency (for pg_statviz) on RHEL 10, Amazon Linux 2023 and
  SLES 16. Per https://github.com/pgdg-packaging/pgdg-rpms/issues/249
- Add RHEL 9 support (python3.12), for pg_statviz. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/249
