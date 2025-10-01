%global python3_sitelib %(%{__python3} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%global	python_runtimes python3

%{?python_disable_dependency_generator}

Summary:	A PostgreSQL client that does auto-completion and syntax highlighting
Name:		pgcli
Version:	4.3.0
Release:	1PGDG%{?dist}
# The exceptions allow linking to OpenSSL and PostgreSQL's libpq
License:	LGPLv3+ with exceptions
Url:		https://github.com/dbcli/%{name}
Source0:	https://github.com/dbcli/%{name}/archive/refs/tags/v%{version}.tar.gz

BuildRequires:	python3-devel

BuildRequires:	python3-pytest python3-sqlparse python3-cli-helpers
BuildRequires:	python3-mock python3-pexpect
BuildRequires:	python3-pgspecial python3-psycopg3
BuildRequires:	python3-setproctitle python3-sshtunnel python3-tzlocal

Requires:	python3-click >= 3.2, python3-pygments >= 2.0
Requires:	python3-sqlparse >= 0.1.14, python3-%{name}
Requires:	python3-jedi >= 0.8.1 python3-setproctitle >= 1.1.9
Requires:	python3-wcwidth >= 0.1.6 python3-humanize >= 0.5.1
Requires:	python3-configobj >= 5.0.6
Requires:	python3-cli-helpers python3-cli-helpers+styles
BuildArch:	noarch

%description
This is a PostgreSQL client that does auto-completion and syntax highlighting.

%package -n python3-%{name}
Summary:	A PostgreSQL client that does auto-completion and syntax highlighting for Python 3

%description -n python3-%{name}
This is a build of pgcli the for the Python 3.

%package -n python3-%{name}-debug
Summary:	A PostgreSQL client that does auto-completion and syntax highlighting for Python 3 (debug build)
# Require base python 3 package, as we're sharing .py/.pyc files:
Requires:	python3-%{name} = %{version}-%{release}

%description -n python3-%{name}-debug
This is a build of the pgcli for the debug build of Python 3.

%prep
%setup -q

%build
%pyproject_wheel

%install
%pyproject_install
%files
%defattr(-,root,root)
%doc AUTHORS changelog.rst LICENSE.txt DEVELOP.rst TODO
%{_bindir}/%{name}

%files -n python3-%{name}
%defattr(-,root,root)
%doc AUTHORS changelog.rst LICENSE.txt DEVELOP.rst TODO
%dir %{python3_sitelib}/%{name}
%{python3_sitelib}/%{name}/*
%{python3_sitelib}/%{name}-%{version}.dist-info/*

%files -n python3-%{name}-debug
%defattr(-,root,root)
%doc LICENSE.txt

%changelog
* Tue Sep 30 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com>
- Change => to >= in Requires and BuildRequires

* Sun Mar 23 2025 Devrim Gündüz <devrim@gunduz.org> - 4.3.0-1PGDG
- Update to 4.3.0

* Fri Aug 23 2024 Devrim Gündüz <devrim@gunduz.org> - 4.1.0-1PGDG
- Update to 4.1.0

* Mon Feb 19 2024 Devrim Gündüz <devrim@gunduz.org> - 4.0.1-1PGDG
- Update to 4.0.1
- Add PGDG branding

* Fri Sep 16 2022 Devrim Gündüz <devrim@gunduz.org> - 3.5.0-1
- Update to 3.5.0

* Sun Mar 6 2022 Devrim Gündüz <devrim@gunduz.org> - 3.4.0-1
- Update to 3.4.0

* Tue Feb 8 2022 Devrim Gündüz <devrim@gunduz.org> - 3.3.1-1
- Update to 3.3.1

* Mon Sep 13 2021 Devrim Gündüz <devrim@gunduz.org> - 3.2.0-1
- Update to 3.2.0

* Fri Sep 27 2019 Devrim Gündüz <devrim@gunduz.org> - 2.1.1-1
- Update to 2.1.1

* Tue Apr 16 2019 Devrim Gündüz <devrim@gunduz.org> - 2.1.0-1
- Update to 2.1.0

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 1.6.0-1.1
- Rebuild against PostgreSQL 11.0

* Tue Jun 6 2017 Devrim Gündüz <devrim@gunduz.org> 1.6.0-1
- Update to 1.6.0

* Mon Sep 19 2016 Devrim Gündüz <devrim@gunduz.org> 1.2.0-1
- Update to 1.2.0
- Fix packaging errors, spec file errors, etc.

* Fri Apr 17 2015 Devrim Gündüz <devrim@gunduz.org> 0.16.3-1
- Initial packaging for PostgreSQL YUM repository.
