%global	modname argh

%if 0%{?fedora} && 0%{?fedora} == 45
%global __ospython %{_bindir}/python3.15
%global python3_pkgversion 3.15
%endif
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
# Build the python311 flavor with the SUSE pyproject macros:
%global	pythons python311
%global	python3_sitelib %{_prefix}/lib/python3.11/site-packages
%endif
%if 0%{?suse_version} == 1600
%global	__ospython %{_bindir}/python3.13
%global	python3_pkgversion 313
%endif

Name:		python%{python3_pkgversion}-%{modname}
# pg_statviz (the only consumer) requires argh < 0.30:
Epoch:		1
Version:	0.29.4
Release:	1PGDG%{?dist}
Summary:	An unobtrusive argparse wrapper with natural syntax

License:	LGPLv3+
URL:		https://pypi.python.org/pypi/%{modname}
Source0:	https://pypi.python.org/packages/source/a/%{modname}/%{modname}-%{version}.tar.gz
Source1:	https://www.gnu.org/licenses/lgpl-3.0.txt
Source2:	https://www.gnu.org/licenses/gpl-3.0.txt
BuildArch:	noarch

BuildRequires:	python%{python3_pkgversion}-devel
BuildRequires:	python%{python3_pkgversion}-flit-core
BuildRequires:	python%{python3_pkgversion}-pip
%if 0%{?suse_version}
BuildRequires:	python-rpm-macros
%else
BuildRequires:	pyproject-rpm-macros
%endif

Provides:	python3-%{modname}%{?_isa} = %{version}-%{release}
Provides:	python%{python3_pkgversion}dist(%{name}) = %{version}-%{release}

%description
Building a command-line interface? Found yourself uttering “argh!” while struggling with the API of argparse? Don’t like the complexity but need the power?
Argh is a smart wrapper for argparse. Argparse is a very powerful tool; Argh just makes it easy to use.


BuildRequires:	python3-devel
BuildRequires:	python3-mock
BuildRequires:	python3-setuptools
BuildRequires:	glibc-langpack-en

%{?python_provide:%python_provide python3-%{modname}}

%prep
%autosetup -n %{modname}-%{version} -p 1

%{__install} -pm 0644 %{SOURCE1} COPYING
%{__install} -pm 0644 %{SOURCE2} .

%build
%pyproject_wheel

%install
%pyproject_install

%files -n python%{python3_pkgversion}-%{modname}
%doc README.rst
%license COPYING gpl-3.0.txt
%{python3_sitelib}/argh*/

%changelog
* Tue Oct 06 2026 Devrim Gunduz <devrim@gunduz.org> - 1:0.29.4-1PGDG
- Downgrade to 0.29.4, and add Epoch to make it an upgrade. pg_statviz,
  the only consumer of this package, requires argh < 0.30: newer argh
  releases have breaking changes, and they have not been tested with
  pg_statviz yet.
- Add missing BR for %%pyproject_wheel macros. Builds failed on RHEL
  and SLES without it.
- Build the python311 flavor on SLES 15.
- Add missing Fedora 45 pin (python3.15)

* Fri Sep 11 2026 Devrim Gunduz <devrim@gunduz.org> - 0.31.3-3PGDG
- Remove Fedora <= 42 support
- Add missing Fedora 44 pin (python3.14)

* Thu Sep 10 2026 Devrim Gunduz <devrim@gunduz.org> - 0.31.3-2PGDG
- Add missing BR

* Mon Aug 31 2026 Devrim Gunduz <devrim@gunduz.org> - 0.31.3-1PGDG
- Update to 0.31.3 per changes described at:
  https://pypi.org/project/argh/0.31.3/

* Tue Aug 25 2026 Devrim Gunduz <devrim@gunduz.org> - 0.29.4-45PGDG
- Also set __python3 (not just __ospython) for Amazon Linux 2023, so
  %pyproject_wheel/%pyproject_install actually build against python3.13
  instead of silently falling back to the system default python3
  (__ospython only affects this repo's own macro computations, not
  RPM's own pyproject/site-packages macros).

* Tue Aug 25 2026 Devrim Gündüz <devrim@gunduz.org> - 0.29.4-44PGDG
- Build against the python3.13 alt-stack on Amazon Linux 2023, to keep
  the Python stack consistent across all packages in the repo.

* Fri May 8 2026 Devrim Gündüz <devrim@gunduz.org> - 0.29.4-43PGDG
- Add missing BR

* Fri Jan 16 2026 Devrim Gündüz <devrim@gunduz.org> - 0.29.4-42PGDG
- Rename package to satisfy pg_statviz dependency on all distros.

* Mon Jul 3 2023 Devrim Gündüz <devrim@gunduz.org> - 0.26.2-1PGDG
- Initial packaging for the PostgreSQL RPM repository to support
  pg_statviz package.
