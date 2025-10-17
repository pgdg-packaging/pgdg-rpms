%global sname mailchimp_fdw
%global packagesoversion 0.3.0

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
%global python_sitelib %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")

Summary:	PostgreSQL foreign data wrapper for Mailchimp
Name:		%{sname}
Version:	0.3.1
Release:	4PGDG%{?dist}
License:	BSD
Source0:	https://github.com/daamien/%{sname}/archive/%{version}.tar.gz
URL:		https://github.com/daamien/%{sname}

BuildArch:	noarch

%description
This is a PostgreSQL FDW for Mailchimp

%prep
%setup -q -n %{sname}-%{version}

%build
%{__ospython} setup.py build

%install
%{__rm} -rf %{buildroot}
%{__ospython} setup.py install -O1 --skip-build --root %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.md
%dir %{python_sitelib}/mailchimpfdw/
%{python_sitelib}/mailchimpfdw-%{packagesoversion}-py%{py3ver}.egg-info
%{python_sitelib}/mailchimpfdw/*.py*
%{python_sitelib}/mailchimpfdw/__pycache__/*.pyc

%changelog
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

