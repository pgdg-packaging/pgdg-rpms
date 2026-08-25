%global sname mailchimp_fdw
%global packagesoversion 0.3.0

%if 0%{?fedora} && 0%{?fedora} == 44
%global __ospython %{_bindir}/python3.14
%global python3_pkgversion 3.14
%endif
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
%if 0%{?amzn} == 2023
%global	__ospython %{_bindir}/python3.13
%global	__python3 %{_bindir}/python3.13
%global	python3_pkgversion 3.13
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
%global python_sitelib %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")

Summary:	PostgreSQL foreign data wrapper for Mailchimp
Name:		%{sname}
Version:	0.3.1
Release:	8PGDG%{?dist}
License:	BSD
Source0:	https://github.com/daamien/%{sname}/archive/%{version}.tar.gz
URL:		https://github.com/daamien/%{sname}

BuildArch:	noarch

%if 0%{?suse_version} >= 1500
BuildRequires:	python-rpm-macros
%else
BuildRequires:	pyproject-rpm-macros
%endif

BuildRequires:	python%{python3_pkgversion}-wheel

%description
This is a PostgreSQL FDW for Mailchimp

%prep
%setup -q -n %{sname}-%{version}

%build
%pyproject_wheel

%install
%pyproject_install

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.md
%dir %{python_sitelib}/mailchimpfdw/
%{python_sitelib}/mailchimpfdw-%{packagesoversion}.dist-info
%{python_sitelib}/mailchimpfdw/*.py*
%{python_sitelib}/mailchimpfdw/__pycache__/*.pyc

%changelog
* Tue Aug 25 2026 Devrim Gunduz <devrim@gunduz.org> - 0.3.1-8PGDG
- Also set __python3 (not just __ospython) for Amazon Linux 2023, so
  %pyproject_wheel/%pyproject_install actually build against python3.13
  instead of silently falling back to the system default python3.
  This one already had its own local sitelib override, so the
  mismatch was active (not just cosmetic): pip would install via 3.9
  while %files looked for files under python3.13's site-packages.

* Tue Aug 25 2026 Devrim Gündüz <devrim@gunduz.org> - 0.3.1-7PGDG
- Build against the python3.13 alt-stack on Amazon Linux 2023, to keep
  the Python stack consistent across all packages in the repo.

* Thu May 7 2026 Devrim Gündüz <devrim@gunduz.org> - 0.3.1-6PGDG
- Add missing BR

* Tue Apr 28 2026 Devrim Gündüz <devrim@gunduz.org> - 0.3.1-5PGDG
- Switch to pyproject builds.
- Add Fedora 44 support, per #167.

* Fri Oct 17 2025 Devrim Gündüz <devrim@gunduz.org> - 0.3.1-4PGDG
- Fix builds with Python 3.1x

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 0.3.1-3PGDG
- Enable builds on Python 3.10+
- Add PGDG branding
- Minor spec file cleanup

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 0.3.1-2.1
- Rebuild against PostgreSQL 11.0

* Tue May 16 2017 - Devrim Gündüz <devrim@gunduz.org> 0.3.1-2
- Relax dependency on PostgreSQL.

* Wed Dec 30 2015 - Devrim Gündüz <devrim@gunduz.org> 0.3.1-1
- Update to 0.3.1

* Mon Mar 16 2015 - Devrim Gündüz <devrim@gunduz.org> 0.1.0-1
- Initial RPM packaging for PostgreSQL RPM Repository

