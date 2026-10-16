%if 0%{?fedora} && 0%{?fedora} == 44
%global __ospython %{_bindir}/python3.14
%global python3_pkgversion 3.14
%endif
%if 0%{?fedora} && 0%{?fedora} == 43
%global __ospython %{_bindir}/python3.14
%global python3_pkgversion 3.14
%endif
%if 0%{?rhel} && 0%{?rhel} <= 10
%global	__ospython %{_bindir}/python3.12
%global	python3_pkgversion 3.12
%endif
%if 0%{?amzn} == 2023
%global	__ospython %{_bindir}/python3.13
%global	__python3 %{_bindir}/python3.13
%global	python3_pkgversion 3.13
%endif
%if 0%{?suse_version} == 1500
%global	__ospython %{_bindir}/python3.11
%global	python3_pkgversion 311
# Build the python311 flavor with the SUSE pyproject macros, instead of
# the default python3 (3.6):
%global	pythons python311
%global	python3_sitearch %{_libdir}/python3.11/site-packages
%endif
%if 0%{?suse_version} == 1600
%global	__ospython %{_bindir}/python3.13
%global	python3_pkgversion 313
%endif

%if 0%{?amzn} == 2023
Name:		python%{python3_pkgversion}-snappy
%else
Name:		python3-snappy
%endif
Epoch:		1
Version:	0.6.1
Release:	3PGDG%{dist}
Summary:	Python library for the snappy compression library
License:	BSD-3-Clause
URL:		https://github.com/andrix/python-snappy
Source:		https://files.pythonhosted.org/packages/source/p/python-snappy/python-snappy-%{version}.tar.gz

%if 0%{?amzn} == 2023
BuildRequires:	gcc-c++ pkgconfig snappy-devel
BuildRequires:	python%{python3_pkgversion}-devel python%{python3_pkgversion}-packaging
BuildRequires:	python%{python3_pkgversion}-pip python%{python3_pkgversion}-setuptools
BuildRequires:	python%{python3_pkgversion}-cffi python%{python3_pkgversion}-wheel
%else
BuildRequires:	gcc-c++ pkgconfig python3-packaging python3-pip
BuildRequires:	python3-setuptools snappy-devel python3-cffi python3-wheel python3-devel
%endif
%if 0%{?suse_version} >= 1500
BuildRequires:	python-rpm-macros
%else
BuildRequires:	pyproject-rpm-macros
%endif

%if ! 0%{?amzn}
Provides:	python3-%{sname}%{?_isa} = %{version}-%{release}
Provides:	python%{python3_pkgversion}dist(%{name}) = %{version}-%{release}
%endif

%description
Python library for the snappy compression library from Google.

%prep
%setup -q -n python-snappy-%{version}
sed -i -e '/^#!\//, 1d' src/snappy/snappy.py

%build
%pyproject_wheel

%install
%pyproject_install

%files
%doc AUTHORS README.rst
%license LICENSE
%{python3_sitearch}/*

%changelog
* Fri Oct 16 2026 Devrim Gunduz <devrim@gunduz.org> - 1:0.6.1-3PGDG
- Build python3.13-snappy on Amazon Linux 2023, for rohmu and pghoard,
  which are built for Python 3.13 there.

* Sun Oct 11 2026 Devrim Gunduz <devrim@gunduz.org> - 0.6.1-2PGDG
- Build the python311 flavor on SLES 15. The SUSE pyproject macros built
  for the default python3 (3.6), so the build failed there. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/226
- Set python3_sitearch to the python3.11 one on SLES 15, too: the SUSE macro
  points to the default python3 (3.6).

* Mon Sep 14 2026 Devrim Gunduz <devrim@gunduz.org> - 1:0.6.1-1PGDG
- Pin back to 0.6.1: 0.7.x rewrote the compression backend to hard-depend
  on cramjam (Rust-based), which isn't packaged anywhere in SLES 15/16
  repos and would need a Rust/cargo toolchain to build from source. 0.6.1
  is the last release using the system libsnappy via CFFI directly,
  matching our existing BuildRequires (snappy-devel, gcc-c++). Added
  Epoch to ensure this is treated as an upgrade over the previously
  shipped 0.7.3.

* Fri Sep 11 2026 Devrim Gunduz <devrim@gunduz.org> - 0.7.3-3PGDG
- Remove Fedora <= 42 support
- Add missing Fedora 44 pin (python3.14)

* Thu Sep 10 2026 Devrim Gunduz <devrim@gunduz.org> - 0.7.3-2PGDG
- Add missing BR

* Mon Aug 31 2026 Devrim Gunduz <devrim@gunduz.org> - 0.7.3-1PGDG
- Update to 0.7.3 per changes described at:
  https://pypi.org/project/python-snappy/0.7.3/
- Update Source0 to the renamed python_snappy-0.7.3.tar.gz artifact and
  %setup -n to python_snappy-%{version}, since upstream renamed the
  sdist from python-snappy to python_snappy starting with this release.

* Tue Aug 25 2026 Devrim Gunduz <devrim@gunduz.org> - 0.6.1-44PGDG
- Also set __python3 (not just __ospython) for Amazon Linux 2023, so
  %pyproject_wheel/%pyproject_install actually build against python3.13
  instead of silently falling back to the system default python3
  (__ospython only affects this repo's own macro computations, not
  RPM's own pyproject/site-packages macros).

* Tue Aug 25 2026 Devrim Gündüz <devrim@gunduz.org> - 0.6.1-43PGDG
- Build against the python3.13 alt-stack on Amazon Linux 2023, to keep
  the Python stack consistent across all packages in the repo.

* Sat Oct 25 2025 Devrim Gündüz <devrim@gunduz.org> - 0.6.1-42PGDG
- Add SLES 16 support
- Switch to pyproject build

* Tue Feb 20 2024 Devrim Gündüz <devrim@gunduz.org> - 0.6.1-3PGDG
- Initial packaging for the PostgreSQL RPM repository to support
  pghoard on SLES 15.
