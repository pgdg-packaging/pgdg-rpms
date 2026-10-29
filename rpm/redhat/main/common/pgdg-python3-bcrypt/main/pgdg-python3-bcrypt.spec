%pgdg_python3_setup

# Built for the python3.13 alt-stack of Amazon Linux 2023, for the SFTP
# storage backend of rohmu (pghoard), and for RHEL 10 (the OS Python there),
# for paramiko.

%global	modname bcrypt
%global	pymodname bcrypt

Name:		python%{python3_pkgversion}-%{modname}
Version:	4.3.0
Release:	42PGDG%{?dist}
Summary:	Modern password hashing for your software and your servers

# bcrypt is Apache-2.0. The licenses of the crates that it is built with,
# checked with "cargo tree -e normal" (35 crates for 4.3.0):
License:	Apache-2.0 AND MIT AND (MIT OR Apache-2.0) AND (Unlicense OR MIT) AND BSD-3-Clause AND Apache-2.0 WITH LLVM-exception AND Unicode-3.0
URL:		https://github.com/pyca/bcrypt
Source0:	https://files.pythonhosted.org/packages/source/b/bcrypt/%{pymodname}-%{version}.tar.gz
# The crates that bcrypt depends on, for building without network access.
# Made with "./pgdg-python3-bcrypt-vendor.sh %%{version}", which runs
# cargo-vendor-filterer for the Linux architectures that we build on.
# It has to be made again for every new version.
Source1:	https://download.postgresql.org/pub/repos/yum/rust-sources/%{pymodname}/%{pymodname}-%{version}-vendor.tar.xz

BuildRequires:	python%{python3_pkgversion}-devel
BuildRequires:	pyproject-rpm-macros
BuildRequires:	python%{python3_pkgversion}-pip
BuildRequires:	python%{python3_pkgversion}-setuptools
BuildRequires:	python%{python3_pkgversion}-wheel
BuildRequires:	python%{python3_pkgversion}-setuptools-rust >= 1.7.0
# rust-version in pyproject.toml of this release:
BuildRequires:	rust >= 1.64
BuildRequires:	cargo >= 1.64
BuildRequires:	gcc

%if 0%{?rhel} == 10
# %%pgdg_python3_setup renamed python3-bcrypt to python%%{python3_pkgversion}-bcrypt:
Provides:	python3-%{modname} = %{version}-%{release}
Provides:	python3-%{modname}%{?_isa} = %{version}-%{release}
Obsoletes:	python3-%{modname} < %{version}-%{release}
%endif

%description
Good password hashing for your software and your servers.

%prep
%setup -q -n %{pymodname}-%{version}
# The vendor directory goes next to Cargo.toml of the Rust extension:
tar -C src/_bcrypt -xf %{SOURCE1}

# Use the vendored crates, and nothing from the network. setuptools-rust
# runs cargo in the top directory:
mkdir -p .cargo
cat > .cargo/config.toml <<'CARGOEOF'
[source.crates-io]
replace-with = "vendored-sources"

[source.vendored-sources]
directory = "src/_bcrypt/vendor"
CARGOEOF

%build
export CARGO_HOME="$PWD/.cargo-home"
export CARGO_NET_OFFLINE=true
# Keep the debug information for the debuginfo package:
export CARGO_PROFILE_RELEASE_DEBUG=2
export CARGO_PROFILE_RELEASE_STRIP=none
%{?build_rustflags:export RUSTFLAGS="%{build_rustflags}"}
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files -l bcrypt

%files -f %{pyproject_files}
%doc README.rst

%changelog
* Thu Oct 29 2026 Devrim Gunduz <devrim@gunduz.org> - 4.3.0-42PGDG
- Update to 4.3.0, which is written in Rust, with its own vendored crates
  tarball. On RHEL 10, 3.2.2 was older than EPEL's 4.3.0. Not 5.0.0 yet:
  its hashpw() raises ValueError for passwords longer than 72 bytes,
  instead of truncating them as before. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/422

* Wed Oct 28 2026 Devrim Gunduz <devrim@gunduz.org> - 3.2.2-43PGDG
- Use %%pgdg_python3_setup from pgdg-srpm-macros 2.5.0 instead of the
  per-distro Python block and the __ospython macro. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/462
- On RHEL 10, the package is now python3.12-bcrypt, which provides
  and obsoletes python3-bcrypt.

* Sat Oct 24 2026 Devrim Gunduz <devrim@gunduz.org> - 3.2.2-42PGDG
- Add RHEL 10 support, without EPEL. Start the release from 42, so that our
  packages win over EPEL's. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/422

* Fri Oct 16 2026 Devrim Gunduz <devrim@gunduz.org> - 3.2.2-1PGDG
- Initial packaging for the PostgreSQL RPM repository, for
  the SFTP storage backend of rohmu (pghoard) on Amazon Linux 2023.
