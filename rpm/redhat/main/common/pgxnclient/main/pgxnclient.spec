%global debug_package %{nil}

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

%{expand: %%global pyver %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:4])"`)}
%global python3_sitelib %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")

Summary:	Command line tool designed to interact with the PostgreSQL Extension Network
Name:		pgxnclient
Version:	1.3.2
Release:	5PGDG%{?dist}
Source0:	https://pypi.python.org/packages/source/p/%{name}/%{name}-%{version}.tar.gz
License:	BSD
Url:		https://github.com/pgxn/%{name}
BuildRequires:	python%{python3_pkgversion}-devel python%{python3_pkgversion}-setuptools
Requires:	python%{python3_pkgversion}

%description
The PGXN Client is a command line tool designed to interact with the
PostgreSQL Extension Network allowing searching, compiling, installing and
removing extensions in a PostgreSQL installation or database.

%prep
%setup -q -n %{name}-%{version}

%build
%pyproject_wheel

%install
%pyproject_install


%files
%defattr(-,root,root)
%doc docs/
%license COPYING
%dir %{python3_sitelib}/
%dir %{python3_sitelib}/%{name}
%{_bindir}/pgxn
%{_bindir}/%{name}
%{python3_sitelib}/%{name}/*.py*
%{python3_sitelib}/%{name}/utils/*.py*
%{python3_sitelib}/%{name}/commands/*.py*
%{python3_sitelib}/%{name}/libexec/*
%{python3_sitelib}/%{name}-%{version}.dist-info/
%{python3_sitelib}/%{name}/__pycache__/*.p*
%{python3_sitelib}/%{name}/commands/__pycache__/*.p*
%{python3_sitelib}/%{name}/utils/__pycache__/*.p*

%changelog
* Thu Oct 16 2025 Devrim Gündüz <devrim@gunduz.org> 1.3.2-5PGDG
- Switch to pyproject builds.
- Add SLES 16 support

* Wed May 28 2025 Devrim Gündüz <devrim@gunduz.org> 1.3.2-4PGDG
- Add RHEL 10 support

* Mon Aug 21 2023 Devrim Gündüz <devrim@gunduz.org> 1.3.2-3PGDG
- Remove RHEL 6 bits
- Add PGDG branding

* Sun Mar 6 2022 Devrim Gündüz <devrim@gunduz.org> 1.3.2-2
- Fix builds with Fedora 35, and also use the standard macros.

* Fri Sep 10 2021 Devrim Gündüz <devrim@gunduz.org> 1.3.2-1
- Update to 1.3.2

* Mon Oct 7 2019 Devrim Gündüz <devrim@gunduz.org> 1.3-1
- Update to 1.3

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 1.2.1-2.1
- Rebuild against PostgreSQL 11.0

* Tue Jan 26 2016 Devrim Gündüz <devrim@gunduz.org> 1.2.1-2
- Cosmetic improvements to simplify spec file.

* Thu Sep 26 2013 Jeff Frost <jeff@pgexperts.com> 1.2.1-1
- Update to 1.2.1

* Sat Sep 29 2012 Devrim Gündüz <devrim@gunduz.org> 1.2-1
- Update to 1.2

* Fri Jul 27 2012 Devrim Gündüz <devrim@gunduz.org> 1.1-1
- Update to 1.1

* Mon Nov 28 2011 Devrim Gündüz <devrim@gunduz.org> 1.0-1
- Initial packaging for PostgreSQL RPM Repository
