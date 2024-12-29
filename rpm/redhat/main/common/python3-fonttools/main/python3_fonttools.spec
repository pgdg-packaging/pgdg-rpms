%global sname	fonttools
%global pname	fontTools

%{expand: %%global py3ver %(echo `%{__python3} -c "import sys; sys.stdout.write(sys.version[:3])"`)}

Name:		python3-%{pname}
Summary:	Tools to manipulate font files
Version:	4.55.3
Release:	1PGDG%{?dist}
URL:		https://github.com/%{sname}/%{sname}
Source0:	https://github.com/%{sname}/%{sname}/archive/%{version}/%{sname}-%{version}.tar.gz
License:	MIT


BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-setuptools_scm

BuildRequires:  python3-Cython
BuildRequires:  gcc

Requires:	python3-brotli
Requires:	python3-munkres
Requires:       python3-lxml
Requires:       python3-scipy
Requires:       python3-fs

%description
fontTools is a library for manipulating fonts, written in Python. The project
includes the TTX tool, that can convert TrueType and OpenType fonts to and
from an XML text format, which is also called TTX. It supports TrueType,
OpenType, AFM and to an extent Type 1 and some Mac-specific formats.

%prep
%setup -q -n %{sname}-%{version}
%{__rm} -rf *.egg-info

sed -i '1d' Lib/fontTools/mtiLib/__init__.py

%build
export FONTTOOLS_WITH_CYTHON=1
%py3_build

%install
%{__python3} setup.py install --skip-build --root %{buildroot}

# Remove unneeded files:
%{__rm} -f %{buildroot}%{_bindir}/*
%{__rm} -f %{buildroot}%{_mandir}/man1/*

%clean
%{__rm} -rf %{buildroot}

%files
%license LICENSE
%doc NEWS.rst README.rst
%{python3_sitearch}/fontTools
%{python3_sitearch}/%{sname}-%{version}-py%{py3ver}.egg-info

%changelog
* Sun Dec 29 2024 - Devrim Gündüz <devrim@gunduz.org> 4.55.3-1PGDG
- Initial packaging for PostgreSQL RPM repository, to satisfy
  pg_chameleon dependency on SLES 15.
