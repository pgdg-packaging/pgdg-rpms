%global sname	rollbar

%if 0%{?fedora} && 0%{?fedora} == 43
%global python3_pkgversion 3.14
%endif
%if 0%{?fedora} && 0%{?fedora} <= 42
%global	python3_pkgversion 3.13
%endif
%if 0%{?rhel} && 0%{?rhel} <= 10
%global	python3_pkgversion 3.12
%endif
%if 0%{?suse_version} == 1500
%global	python3_pkgversion 311
%endif
%if 0%{?suse_version} == 1600
%global	python3_pkgversion 313
%endif

Name:		python3-%{sname}
Summary:	Python notifier for reporting exceptions, errors, and log messages to Rollbar.
Version:	0.16.2
Release:	43PGDG%{?dist}
URL:		https://github.com/%{sname}/py%{sname}
Source0:	https://github.com/%{sname}/py%{sname}/archive/v%{version}.tar.gz
License:	Python-2.0
BuildArch:	noarch

BuildRequires:	python%{python3_pkgversion}-devel
%if 0%{?suse_version} >= 1500
BuildRequires:	python-rpm-macros
%else
BuildRequires:	pyproject-rpm-macros
%endif

Requires:	python%{python3_pkgversion}-%{name}
Requires:	python3-requests

Provides:	python3-%{sname}%{?_isa} = %{version}-%{release}
Provides:	python%{python3_pkgversion}dist(%{name}) = %{version}-%{release}
Provides:	python%{python3_pkgversion}-python3-%{sname}

%description
The rollbar module makes it easy to write user friendly command line interfaces.

The program defines what arguments it requires, and rollbar will figure out how
to parse those out of sys.argv. The rollbar module also automatically generates
help and usage messages and issues errors when users give the program invalid
arguments.

As of Python >= 2.7 and >= 3.2, the rollbar module is maintained within the
Python standard library. For users who still need to support Python < 2.7
or < 3.2, it is also provided as a separate package, which tries to stay
compatible with the module in the standard library, but also supports older
Python versions.

%prep
%setup -q -n pyrollbar-%{version}

%build
%pyproject_wheel

%install
%pyproject_install

%files
%{_bindir}/%{sname}
%{python3_sitelib}/%{sname}-%{version}.dist-info/*
%{python3_sitelib}/%{sname}/__pycache__/*.py*
%{python3_sitelib}/%{sname}/*.py*
%{python3_sitelib}/%{sname}/contrib/*.py*
%{python3_sitelib}/%{sname}/contrib/__pycache__/*py*
%{python3_sitelib}/%{sname}/contrib/asgi/*.py*
%{python3_sitelib}/%{sname}/contrib/asgi/__pycache__/*.py*
%{python3_sitelib}/%{sname}/contrib/bottle/*.py*
%{python3_sitelib}/%{sname}/contrib/bottle/__pycache__/*.py*
%{python3_sitelib}/%{sname}/contrib/django/*.py*
%{python3_sitelib}/%{sname}/contrib/django/__pycache__/*.py*
%{python3_sitelib}/%{sname}/contrib/django_rest_framework/*.py*
%{python3_sitelib}/%{sname}/contrib/django_rest_framework/__pycache__/*.py*
%{python3_sitelib}/%{sname}/contrib/fastapi/*.py*
%{python3_sitelib}/%{sname}/contrib/fastapi/__pycache__/*.py*
%{python3_sitelib}/%{sname}/contrib/flask/*.py*
%{python3_sitelib}/%{sname}/contrib/flask/__pycache__/*.py*
%{python3_sitelib}/%{sname}/contrib/pyramid/*.py*
%{python3_sitelib}/%{sname}/contrib/pyramid/__pycache__/*.py*
%{python3_sitelib}/%{sname}/contrib/quart/*.py*
%{python3_sitelib}/%{sname}/contrib/quart/__pycache__/*.py*
%{python3_sitelib}/%{sname}/contrib/starlette/*.py*
%{python3_sitelib}/%{sname}/contrib/starlette/__pycache__/*.py*
%{python3_sitelib}/%{sname}/contrib/rq/*.py*
%{python3_sitelib}/%{sname}/contrib/rq/__pycache__/*.py*
%{python3_sitelib}/%{sname}/lib/*.py*
%{python3_sitelib}/%{sname}/lib/__pycache__/*.py*
%{python3_sitelib}/%{sname}/lib/filters/*.py*
%{python3_sitelib}/%{sname}/lib/filters/__pycache__/*.py*
%{python3_sitelib}/%{sname}/lib/transforms/__pycache__/*.py*
%{python3_sitelib}/%{sname}/lib/transforms/*.py*
%{python3_sitelib}/%{sname}/test/*/*.py*
%{python3_sitelib}/%{sname}/test/*.py*
%{python3_sitelib}/%{sname}/test/*/__pycache__/*.py*

%changelog
* Thu Oct 30 2025 - Devrim Gündüz <devrim@gunduz.org> 0.16.2-43PGDG
- Add new Provides: for a smoother upgrade.
- Switch to pyproject build

* Sat Oct 25 2025 - Devrim Gündüz <devrim@gunduz.org> 0.16.2-42PGDG
- Add SLES 16 support

* Tue Dec 17 2024 - Devrim Gündüz <devrim@gunduz.org> 0.16.2-2PGDG
- Add RHEL 10 support
- Add PGDG branding

* Mon Feb 7 2022 - Devrim Gündüz <devrim@gunduz.org> 0.16.2-1
- Update to 0.16.2

* Wed Dec 9 2020 - Devrim Gündüz <devrim@gunduz.org> 0.15.1-1
- Initial packaging for PostgreSQL RPM repository, to satisfy
  pg_chameleon dependency.
