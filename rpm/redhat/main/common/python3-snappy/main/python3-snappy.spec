%if 0%{?fedora} && 0%{?fedora} == 43
%global __ospython %{_bindir}/python3.14
%global python3_pkgversion 3.14
%endif
%if 0%{?fedora} && 0%{?fedora} <= 42
%global	__ospython %{_bindir}/python3.13
%global	python3_pkgversion 3.13
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
%endif
%if 0%{?suse_version} == 1600
%global	__ospython %{_bindir}/python3.13
%global	python3_pkgversion 313
%endif

Name:		python3-snappy
Version:	0.7.3
Release:	1PGDG%{dist}
Summary:	Python library for the snappy compression library
License:	BSD-3-Clause
URL:		https://github.com/andrix/python-snappy
Source:		https://files.pythonhosted.org/packages/39/66/9185fbb6605ba92716d9f77fbb13c97eb671cd13c3ad56bd154016fbf08b/python_snappy-%{version}.tar.gz

BuildRequires:	gcc-c++ pkgconfig snappy-devel
%if 0%{?suse_version} >= 1500
BuildRequires:	python-rpm-macros
%else
BuildRequires:	pyproject-rpm-macros
%endif

Provides:	python3-%{sname}%{?_isa} = %{version}-%{release}
Provides:	python%{python3_pkgversion}dist(%{name}) = %{version}-%{release}

%description
Python library for the snappy compression library from Google.

%prep
%setup -q -n python_snappy-%{version}
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
