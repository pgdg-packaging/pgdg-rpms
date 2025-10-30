%global lcname	pygresql

%if 0%{?fedora} >= 41 || 0%{?rhel} >= 10 || 0%{?suse_version} >= 1600
%{expand: %%global py3ver %(echo `%{__python3} -c "import sys; sys.stdout.write(sys.version[:4])"`)}
%else
%{expand: %%global py3ver %(echo `%{__python3} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%endif

Name:		PyGreSQL
Version:	6.1.0
Release:	4PGDG%{?dist}
Summary:	A Python client library for PostgreSQL

URL:		http://www.PyGreSQL.org/
# Author states his intention is to dual license under PostgreSQL or Python
# licenses --- this is not too clear from the current tarball documentation,
# but hopefully will be clearer in future releases.
# The PostgreSQL license is very similar to other MIT licenses, but the OSI
# recognizes it as an independent license, so we do as well.
License:	PostgreSQL or Python

Source0:	https://github.com/%{name}/%{name}/archive/refs/tags/%{version}.tar.gz

Provides:	python3-%{name} = %{version}-%{release}
Provides:	python3-%{name}%{?_isa} = %{version}-%{release}
%{?python_provide:%python_provide python2-%{name}}

BuildRequires:	postgresql%{pgmajorversion}-devel python3-devel
BuildRequires:	libpq5-devel
%if 0%{?suse_version} >= 1500
BuildRequires:	python-rpm-macros
%else
BuildRequires:	pyproject-rpm-macros
%endif

Requires:	libpq5

%description
PostgreSQL is an advanced Object-Relational database management system.
The PyGreSQL package provides a module for developers to use when writing
Python code for accessing a PostgreSQL database.

%prep
%setup -q -n %{name}-%{version}

# PyGreSQL releases have execute bits on all files
find -type f -exec chmod 644 {} +

%build
%pyproject_wheel

%install
%pyproject_install

%files
%license docs/copyright.rst
%doc docs/*.rst
%if 0%{?fedora} >= 43
%{python3_sitearch}/%{lcname}-%{version}.dist-info/
%else
%{python3_sitearch}/%{name}-%{version}.dist-info/
%endif
%{python3_sitearch}/pg/*py*
%{python3_sitearch}/pgdb/*py*

%changelog
* Thu Oct 30 2025 Devrim Gündüz <devrim@gunduz.org> - 6.1.0-4PGDG
- Fix builds against Python 3.14 on Fedora 43

* Fri Oct 17 2025 Devrim Gündüz <devrim@gunduz.org> - 6.1.0-3PGDG
- Add SLES 16 support
- Switch to pyproject builds

* Mon Apr 14 2025 Devrim Gündüz <devrim@gunduz.org> - 6.1.0-2PGDG
- Add RHEL 10 support

* Fri Dec 6 2024 Devrim Gündüz <devrim@gunduz.org> - 6.1.0-1PGDG
- Update to 6.1.0 per changes described at:
  https://pygresql.org/contents/changelog.html

* Thu Oct 26 2023 Devrim Gündüz <devrim@gunduz.org> - 6.0.1-1PGDG
- Update to 6.0.1 per changes described at:
  https://pygresql.org/contents/changelog.html

* Thu Oct 26 2023 Devrim Gündüz <devrim@gunduz.org> - 6.0-1PGDG
- Update to 6.0

* Sat Sep 2 2023 Devrim Gündüz <devrim@gunduz.org> - 5.2.5-1
- Update to 5.2.5
- Add PGDG branding

* Tue Dec 6 2022 Devrim Gündüz <devrim@gunduz.org> - 5.2.3-2
- Remove Advance Toolchain support from RHEL 7 - ppc64le.

* Tue Feb 1 2022 Devrim Gündüz <devrim@gunduz.org> - 5.2.3-1
- Update to 5.2.3

* Tue Apr 20 2021 Devrim Gündüz <devrim@gunduz.org> - 5.2.2-1
- Update to 5.2.2
- Use our own libpq5(-devel)

* Sun Sep 27 2020 Devrim Gündüz <devrim@gunduz.org> - 5.2.1-1
- Update to 5.2.1

* Thu Aug 20 2020 Devrim Gündüz <devrim@gunduz.org> - 5.2-1
- Update to 5.2
- Use only PY3

* Thu Sep 26 2019 Devrim Gündüz <devrim@gunduz.org> - 5.1-1.1
- Rebuild for PostgreSQL 12

* Fri Sep 6 2019 Devrim Gündüz <devrim@gunduz.org> - 5.1-1
- Update to 5.1

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 5.0.6-2.1
- Rebuild against PostgreSQL 11.0

* Tue Aug 28 2018 Devrim Gündüz <devrim@gunduz.org> - 5.0.6-2
- Attemp to fix SLES builds.

* Thu Aug 23 2018 Devrim Gündüz <devrim@gunduz.org> - 5.0.6-1
- Update to 5.0.6
- Spec file cleanup, that refers to very old releases.

* Wed Jan 25 2017 Devrim Gündüz <devrim@gunduz.org> - 5.0.3-1
- Initial build for PostgreSQL YUM repository, based on Fedora spec.
