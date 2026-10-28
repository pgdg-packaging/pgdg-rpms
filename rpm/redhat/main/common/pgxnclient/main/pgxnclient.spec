%pgdg_python3_setup

%{expand: %%global pyver %(echo `%{__python3} -c "import sys; sys.stdout.write(sys.version[:4])"`)}
%global python3_sitelib %(%{__python3} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")

Summary:	Command line tool designed to interact with the PostgreSQL Extension Network
Name:		pgxnclient
Version:	1.3.2
Release:	12PGDG%{?dist}
Source0:	https://pypi.python.org/packages/source/p/%{name}/%{name}-%{version}.tar.gz
License:	BSD
Url:		https://github.com/pgxn/%{name}
BuildRequires:	python%{python3_pkgversion}-devel python%{python3_pkgversion}-setuptools
BuildRequires:	python%{python3_pkgversion}-pip python%{python3_pkgversion}-wheel

Requires:	python%{python3_pkgversion}

BuildArch:	noarch

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
* Wed Oct 28 2026 Devrim Gunduz <devrim@gunduz.org> - 1.3.2-12PGDG
- Use %%pgdg_python3_setup from pgdg-srpm-macros 2.5.0 instead of the
  per-distro Python block and the __ospython macro. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/462

* Sun Oct 11 2026 Devrim Gunduz <devrim@gunduz.org> - 1.3.2-11PGDG
- Build the python311 flavor on SLES 15. The SUSE pyproject macros built
  for the default python3 (3.6), so the build failed there. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/226

* Wed Sep 9 2026 Devrim Gunduz <devrim@gunduz.org> - 1.3.2-10PGDG
- Mark this package as noarch.

* Tue Aug 25 2026 Devrim Gunduz <devrim@gunduz.org> - 1.3.2-9PGDG
- Also set __python3 (not just __ospython) for Amazon Linux 2023, so
  %%pyproject_wheel/%%pyproject_install actually build against python3.13
  instead of silently falling back to the system default python3.
  This one already had its own local sitelib override, so the
  mismatch was active (not just cosmetic): pip would install via 3.9
  while %%files looked for files under python3.13's site-packages.

* Tue Aug 25 2026 Devrim Gündüz <devrim@gunduz.org> 1.3.2-8PGDG
- Build against the python3.13 alt-stack on Amazon Linux 2023, to keep
  the Python stack consistent across all packages in the repo.

* Thu May 7 2026 Devrim Gündüz <devrim@gunduz.org> 1.3.2-7PGDG
- Add missing BRs

* Tue Apr 28 2026 Devrim Gündüz <devrim@gunduz.org> 1.3.2-6PGDG
- Add Fedora 44 support per #167.

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
