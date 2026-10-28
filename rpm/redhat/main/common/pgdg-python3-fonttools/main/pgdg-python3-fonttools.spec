%pgdg_python3_setup

# This spec builds two flavors, depending on the distribution:
#
# - On RHEL 9 and 10 and Amazon Linux 2023: the python3.12 / python3.13
#   flavor (python3.12-fonttools, python3.13-fonttools), for pg_statviz:
#   noarch, without the optional Cython extensions.
# - On SLES: the default python3 flavor (python3-fontTools), with the Cython
#   extensions. This used to be the separate python3-fonttools directory,
#   merged here per https://github.com/pgdg-packaging/pgdg-rpms/issues/369
%global	pgdg_altstack 0
%if ( 0%{?rhel} && 0%{?rhel} <= 10 ) || 0%{?amzn} == 2023
%global	pgdg_altstack 1
%endif

%if %{pgdg_altstack}
%endif

%global	modname fonttools
%global	pymodname fontTools

%if %{pgdg_altstack}
Name:		python%{python3_pkgversion}-%{modname}
Version:	4.67.0
Release:	44PGDG%{?dist}
%else
Name:		python3-%{pymodname}
Version:	4.63.0
Release:	4PGDG%{?dist}
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

%if 0%{?rhel} == 10
# Replace the EPEL package of the same module, which has the same files:
Obsoletes:	python3-fonttools < %{version}-%{release}
%endif

%description
fontTools is a library for manipulating fonts, written in Python. The project
includes the TTX tool, that can convert TrueType and OpenType fonts to and
from an XML text format, which is also called TTX. It supports TrueType,
OpenType, AFM and to an extent Type 1 and some Mac-specific formats.

%if %{pgdg_altstack}
This package is built without the optional Cython extensions.
%endif

%if 0%{?rhel} == 10
%package -n %{modname}
Summary:	Tools to manipulate font files
Requires:	%{name} = %{version}-%{release}
# Replace the EPEL package, which requires EPEL's own python3-fonttools
# version, so it made dnf upgrade fail:
Obsoletes:	%{modname} < %{version}-%{release}

%description -n %{modname}
The fonttools, pyftmerge, pyftsubset and ttx command line tools, which
use %{name}.

%files -n %{modname}
%{_bindir}/fonttools
%{_bindir}/pyftmerge
%{_bindir}/pyftsubset
%{_bindir}/ttx
%{_mandir}/man1/ttx.1*

# EPEL ships these extras metapackages, which require its own python3-fonttools
# version, so they made dnf upgrade fail. Replace them with ours:
%package -n %{name}+graphite
Summary:	Metapackage for %{name}: graphite extras
Requires:	%{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:	python3-fonttools+graphite = %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:	python3-fonttools+graphite < %{?epoch:%{epoch}:}%{version}-%{release}

%description -n %{name}+graphite
This is a metapackage bringing in graphite extras requires for
%{name}. It makes sure the dependencies are installed.

%files -n %{name}+graphite
%ghost %{python3_sitelib}/%{modname}-%{version}.dist-info

%package -n %{name}+interpolatable
Summary:	Metapackage for %{name}: interpolatable extras
Requires:	%{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:	python3-fonttools+interpolatable = %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:	python3-fonttools+interpolatable < %{?epoch:%{epoch}:}%{version}-%{release}

%description -n %{name}+interpolatable
This is a metapackage bringing in interpolatable extras requires for
%{name}. It makes sure the dependencies are installed.

%files -n %{name}+interpolatable
%ghost %{python3_sitelib}/%{modname}-%{version}.dist-info

%package -n %{name}+lxml
Summary:	Metapackage for %{name}: lxml extras
Requires:	%{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:	python3-fonttools+lxml = %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:	python3-fonttools+lxml < %{?epoch:%{epoch}:}%{version}-%{release}

%description -n %{name}+lxml
This is a metapackage bringing in lxml extras requires for
%{name}. It makes sure the dependencies are installed.

%files -n %{name}+lxml
%ghost %{python3_sitelib}/%{modname}-%{version}.dist-info

%package -n %{name}+plot
Summary:	Metapackage for %{name}: plot extras
Requires:	%{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:	python3-fonttools+plot = %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:	python3-fonttools+plot < %{?epoch:%{epoch}:}%{version}-%{release}

%description -n %{name}+plot
This is a metapackage bringing in plot extras requires for
%{name}. It makes sure the dependencies are installed.

%files -n %{name}+plot
%ghost %{python3_sitelib}/%{modname}-%{version}.dist-info

%package -n %{name}+type1
Summary:	Metapackage for %{name}: type1 extras
Requires:	%{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:	python3-fonttools+type1 = %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:	python3-fonttools+type1 < %{?epoch:%{epoch}:}%{version}-%{release}

%description -n %{name}+type1
This is a metapackage bringing in type1 extras requires for
%{name}. It makes sure the dependencies are installed.

%files -n %{name}+type1
%ghost %{python3_sitelib}/%{modname}-%{version}.dist-info

%package -n %{name}+ufo
Summary:	Metapackage for %{name}: ufo extras
Requires:	%{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:	python3-fonttools+ufo = %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:	python3-fonttools+ufo < %{?epoch:%{epoch}:}%{version}-%{release}

%description -n %{name}+ufo
This is a metapackage bringing in ufo extras requires for
%{name}. It makes sure the dependencies are installed.

%files -n %{name}+ufo
%ghost %{python3_sitelib}/%{modname}-%{version}.dist-info

%package -n %{name}+unicode
Summary:	Metapackage for %{name}: unicode extras
Requires:	%{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:	python3-fonttools+unicode = %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:	python3-fonttools+unicode < %{?epoch:%{epoch}:}%{version}-%{release}

%description -n %{name}+unicode
This is a metapackage bringing in unicode extras requires for
%{name}. It makes sure the dependencies are installed.

%files -n %{name}+unicode
%ghost %{python3_sitelib}/%{modname}-%{version}.dist-info

%package -n %{name}+woff
Summary:	Metapackage for %{name}: woff extras
Requires:	%{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:	python3-fonttools+woff = %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:	python3-fonttools+woff < %{?epoch:%{epoch}:}%{version}-%{release}

%description -n %{name}+woff
This is a metapackage bringing in woff extras requires for
%{name}. It makes sure the dependencies are installed.

%files -n %{name}+woff
%ghost %{python3_sitelib}/%{modname}-%{version}.dist-info
%endif

%prep
%autosetup -n %{modname}-%{version}
%if 0%{?rhel} == 10
# The unicode extra wants unicodedata2 >= 18, RHEL 10 (EPEL) has 17. It is
# optional, and only gives fontTools newer Unicode data than Python's:
sed -i 's/"unicodedata2 >= 18.0.0; python_version/"unicodedata2 >= 17.0.0; python_version/' setup.py
grep -q '"unicodedata2 >= 17.0.0; python_version' setup.py
%endif
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
%if 0%{?rhel} == 10
# They go into the fonttools subpackage, which replaces EPEL's:
[ -f %{buildroot}%{_mandir}/man1/ttx.1 ] || \
	%{__install} -D -m 0644 Doc/man/man1/ttx.1 %{buildroot}%{_mandir}/man1/ttx.1
%else
# Remove the scripts and the man page, they conflict with the
# python3-fonttools package of the OS:
%{__rm} -rf %{buildroot}%{_bindir} %{buildroot}%{_mandir}
%endif
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
* Wed Oct 28 2026 Devrim Gunduz <devrim@gunduz.org> - 4.67.0-44PGDG
- Use %%pgdg_python3_setup from pgdg-srpm-macros 2.5.0 instead of the
  per-distro Python block and the __ospython macro. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/462

* Mon Oct 26 2026 Devrim Gunduz <devrim@gunduz.org> - 4.67.0-43PGDG
- RHEL 10: Add the fonttools subpackage with the command line tools, and
  the +graphite, +interpolatable, +lxml, +plot, +type1, +ufo, +unicode and
  +woff extras metapackages. They replace EPEL's, which require its own
  python3-fonttools version, so they made dnf upgrade fail. The +unicode
  one accepts unicodedata2 17 (EPEL) now. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/422

* Sat Oct 24 2026 Devrim Gunduz <devrim@gunduz.org> - 4.67.0-42PGDG
- Add RHEL 10 support, without EPEL: build the python3.12 flavor there, as
  on RHEL 9, and obsolete the EPEL python3-fonttools package. Start the
  release from 42, so that our packages win over EPEL's. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/422

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
