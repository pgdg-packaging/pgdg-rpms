# This spec builds two flavors, depending on the distribution:
#
# - On RHEL 9 and Amazon Linux 2023: the python3.12 / python3.13 alt-stack
#   flavor (python3.12-fonttools, python3.13-fonttools), for pg_statviz:
#   noarch, without the optional Cython extensions.
# - On SLES: the default python3 flavor (python3-fontTools), with the Cython
#   extensions. This used to be the separate python3-fonttools directory,
#   merged here per https://github.com/pgdg-packaging/pgdg-rpms/issues/369
%global	pgdg_altstack 0
%if ( 0%{?rhel} && 0%{?rhel} <= 9 ) || 0%{?amzn} == 2023
%global	pgdg_altstack 1
%endif

%if %{pgdg_altstack}
%if 0%{?rhel}
%global	__ospython %{_bindir}/python3.12
%global	__python3 %{_bindir}/python3.12
%global	python3_pkgversion 3.12
%endif
%if 0%{?amzn} == 2023
%global	__ospython %{_bindir}/python3.13
%global	__python3 %{_bindir}/python3.13
%global	python3_pkgversion 3.13
%endif
%endif

%global	modname fonttools
%global	pymodname fontTools

%if %{pgdg_altstack}
Name:		python%{python3_pkgversion}-%{modname}
Version:	4.67.0
Release:	1PGDG%{?dist}
%else
Name:		python3-%{pymodname}
Version:	4.63.0
Release:	3PGDG%{?dist}
%endif
Summary:	Tools to manipulate font files

License:	MIT
URL:		https://github.com/%{modname}/%{modname}
%if %{pgdg_altstack}
Source0:	https://files.pythonhosted.org/packages/source/f/%{modname}/%{modname}-%{version}.tar.gz
BuildArch:	noarch
%else
Source0:	https://github.com/%{modname}/%{modname}/archive/%{version}/%{modname}-%{version}.tar.gz
%endif

%if %{pgdg_altstack}
BuildRequires:	python%{python3_pkgversion}-devel
BuildRequires:	pyproject-rpm-macros
BuildRequires:	python%{python3_pkgversion}-pip
BuildRequires:	python%{python3_pkgversion}-setuptools
BuildRequires:	python%{python3_pkgversion}-wheel
%else
BuildRequires:	python3-devel
BuildRequires:	python3-setuptools
BuildRequires:	python3-setuptools_scm
BuildRequires:	python3-Cython
BuildRequires:	gcc

Requires:	python3-munkres
Requires:	python3-lxml
Requires:	python3-scipy
Requires:	python3-fs
%endif

%description
fontTools is a library for manipulating fonts, written in Python. The project
includes the TTX tool, that can convert TrueType and OpenType fonts to and
from an XML text format, which is also called TTX. It supports TrueType,
OpenType, AFM and to an extent Type 1 and some Mac-specific formats.

%if %{pgdg_altstack}
This package is built without the optional Cython extensions.
%endif

%prep
%autosetup -n %{modname}-%{version}
%if ! %{pgdg_altstack}
%{__rm} -rf *.egg-info
sed -i '1d' Lib/fontTools/mtiLib/__init__.py
# Do not pass the freethreading_compatible directive to Cython on Python
# >= 3.13: it needs Cython >= 3.1, which is newer than the Cython of SLES.
# It only matters for the free-threaded Python builds, which SLES does
# not ship:
sed -i '/directives\["freethreading_compatible"\] = True/d; /if sys.version_info >= (3, 13):$/d' setup.py
%endif

%build
%if %{pgdg_altstack}
# Do not build the optional Cython extensions, even when Cython is
# installed. They need Cython >= 3.1, which is newer than the Cython of
# some distros (AL2023 has 3.0):
export FONTTOOLS_WITH_CYTHON=0
%pyproject_wheel
%else
export FONTTOOLS_WITH_CYTHON=1
%py3_build
%endif

%install
%if %{pgdg_altstack}
%pyproject_install
# Remove the scripts and the man page, they conflict with the
# python3-fonttools package of the OS:
%{__rm} -rf %{buildroot}%{_bindir} %{buildroot}%{_mandir}
%else
%{__python3} setup.py install --skip-build --root %{buildroot}
# Remove unneeded files:
%{__rm} -f %{buildroot}%{_bindir}/*
%{__rm} -f %{buildroot}%{_mandir}/man1/*
%endif

%files
%if %{pgdg_altstack}
%license LICENSE LICENSE.external
%doc README.rst
%{python3_sitelib}/%{pymodname}/
%{python3_sitelib}/%{modname}-%{version}.dist-info/
%else
%license LICENSE
%doc NEWS.rst README.rst
%{python3_sitearch}/%{pymodname}
%{python3_sitearch}/%{modname}-%{version}-py%{python3_version}.egg-info
%endif

%changelog
* Thu Oct 15 2026 Devrim Gunduz <devrim@gunduz.org> - 4.63.0-3PGDG
- SLES: Fix "unknown compiler directive: freethreading_compatible" build
  failure with Python 3.13: do not pass that directive to Cython, it needs
  Cython >= 3.1.
- SLES: Use %%{python3_version} in the egg-info directory name. The
  sys.version[:3] construct returned "3.1" on Python 3.13.

* Thu Oct 15 2026 Devrim Gunduz <devrim@gunduz.org> - 4.67.0-1PGDG
- Update to 4.67.0 on RHEL 9 and Amazon Linux 2023, per changes described
  at https://github.com/fonttools/fonttools/releases/tag/4.67.0
  Per https://github.com/pgdg-packaging/pgdg-rpms/issues/379
- Give each flavor its own Release, so that the SLES (4.63.0) builds keep
  2PGDG.

* Thu Oct 08 2026 Devrim Gunduz <devrim@gunduz.org> - 4.66.1-2PGDG
- Do not build the Cython extensions when Cython is installed, they
  need Cython >= 3.1.

* Tue Oct 06 2026 Devrim Gunduz <devrim@gunduz.org> - 4.66.1-1PGDG
- Initial packaging for the PostgreSQL RPM repository, to satisfy
  pg_statviz dependency on Amazon Linux 2023.
- Add RHEL 9 support (python3.12), for pg_statviz. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/249

* Mon Sep 14 2026 Devrim Gündüz <devrim@gunduz.org> - 4.63.0-2PGDG
- Drop the hard Requires on python3-brotli: upstream only lists brotli as
  an optional extra (WOFF2 compression support), not a core dependency,
  and pg_statviz (this package's sole consumer) doesn't need it either.

* Mon Aug 31 2026 Devrim Gündüz <devrim@gunduz.org> - 4.63.0-1PGDG
- Update to 4.63.0 per changes described at:
  https://github.com/fonttools/fonttools/releases/tag/4.63.0

* Sun Dec 29 2024 Devrim Gündüz <devrim@gunduz.org> - 4.55.3-1PGDG
- Initial packaging for PostgreSQL RPM repository, to satisfy
  pg_chameleon dependency on SLES 15.
