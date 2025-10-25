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
%if 0%{?suse_version} == 1500
%global	__ospython %{_bindir}/python3.11
%global	python3_pkgversion 311
%endif
%if 0%{?suse_version} == 1600
%global	__ospython %{_bindir}/python3.13
%global	python3_pkgversion 313
%endif

%{expand: %%global py3ver %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:4])"`)}

%global python3_sitelib %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")


Name:		python3-plac
Version:	1.3.5
Release:	42PGDG%{?dist}
Summary:	The smartest command line arguments parser in the world
License:	BSD-2-Clause
URL:		https://github.com/ialbert/plac
Source0:	https://github.com/ialbert/plac/archive/v%{version}/plac-%{version}.tar.gz
# Man page written for Fedora in groff_man(7) format based on --help output
Source1:	plac_runner.py.1

BuildArch:	noarch

BuildRequires:	python%{python3_pkgversion}-devel
Requires:	python%{python3_pkgversion}-%{name}

Provides:	python3-%{sname}%{?_isa} = %{version}-%{release}
Provides:	python%{python3_pkgversion}dist(%{name}) = %{version}-%{release}

%description
plac is a Python package that can generate command line parameters from
function signatures.

plac works on Python 2.6 through all versions of Python 3.

plac has no dependencies beyond modules already present in the Python standard
library.

plac implements most of its functionality in a single file that may be included
in your source code.}

%prep
%setup -q -n plac-%{version}

%build
%{__ospython} setup.py build

%install
%{__ospython} setup.py install --no-compile --root %{buildroot}

# Install man file
%{__install} -t '%{buildroot}%{_mandir}/man1' -m 0644 -p -D '%{SOURCE1}'

# Create __pycache__ directories and their contents in SLES *too*:
%if 0%{?suse_version}
%py3_compile %{buildroot}%{python3_sitelib}
%endif

%files
%doc CHANGES.md README.md RELEASE.md
%{_bindir}/plac_runner.py
%{_mandir}/man1/plac_runner.py.1*
%dir %{python3_sitelib}/%{sname}-%{version}-py%{py3ver}.egg-info
%{python3_sitelib}/%{sname}-%{version}-py%{py3ver}.egg-info/*
%{python3_sitelib}/%{sname}*py
%{python3_sitelib}/__pycache__/%{sname}*pyc

%changelog
* Sat Oct 25 Devrim Gündüz <devrim@gunduz.org> - 1.3.5-42PGDG
- Add SLES 16 support

* Wed Dec 18 2024 Devrim Gündüz <devrim@gunduz.org> - 1.3.5-2PGDG
- Add RHEL 10 support

* Tue Feb 20 2024 Devrim Gündüz <devrim@gunduz.org> - 1.3.5-1PGDG
- Initial packaging for the PostgreSQL RPM repository to support
  pg_statviz on RHEL 8 and SLES 15.
