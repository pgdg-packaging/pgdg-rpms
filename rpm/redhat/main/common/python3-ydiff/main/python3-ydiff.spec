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
%if 0%{?suse_version} >= 1500
%global	__ospython %{_bindir}/python3.11
%global	python3_pkgversion 311
%endif

%{expand: %%global py3ver %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:4])"`)}
%global python3_sitelib %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")

Name:		ydiff
Version:	1.4.2
Release:	46PGDG%{?dist}.1
Summary:	View colored, incremental diff
URL:		https://github.com/ymattw/%{name}
License:	BSD
Source0:	https://github.com/ymattw/%{name}/archive/%{version}/%{name}-%{version}.tar.gz
BuildRequires:	python%{python3_pkgversion}-devel
BuildArch:	noarch

Requires:	less
Requires:	python%{python3_pkgversion}-%{name}

Provides:	python%{python3_pkgversion}dist(ydiff)

%description
Term based tool to view colored, incremental diff in a Git/Mercurial/Svn
workspace or from stdin, with side by side (similar to diff -y) and auto
pager support.

%package -n	python3-%{name}
Summary:	%{summary}
%if 0%{?fedora} >= 40 || 0%{?rhel} >= 9 || 0%{?suse_version} >= 1500
%{?python_provide:%python_provide python3-%{name}}
%endif
%description -n	python3-%{name}
Python library that implements API used by ydiff tool.

%prep
%autosetup -n %{name}-%{version}
%{_bindir}/sed -i '/#!\/usr\/bin\/env python/d' ydiff.py

%build
%{__ospython} setup.py build

%install
%{__rm} -rf %{buildroot}
%{__ospython} setup.py install --root %{buildroot} -O1 --skip-build

%files
%doc README.rst
%license LICENSE
%{_bindir}/%{name}

%files -n python3-%{name}
%{python3_sitelib}/__pycache__/*
%{python3_sitelib}/%{name}.py
%{python3_sitelib}/%{name}-%{version}-py%{py3ver}.egg-info

%changelog
* Mon Sep 22 2025 Devrim Gunduz <devrim@gunduz.org> - 1.4.2-46PGDG.1
- Add Fedora 43 support

* Wed May 21 2025 Devrim Gündüz <devrim@gunduz.org> - 1.4.2-46PGDG
- Rebuild the package per:
  https://github.com/pgdg-packaging/pgdg-rpms/issues/18

* Tue May 20 2025 Devrim Gündüz <devrim@gunduz.org> - 1.4.2-45PGDG
- Add missing Provides

* Sat Apr 19 2025 Devrim Gündüz <devrim@gunduz.org> - 1.4.2-44PGDG
- Build the package with Python 3.12 on RHEL 9 & 8 and Python 3.11 on SLES
  15. For the other distros (Fedora and RHEL 10) use OS'd default Python
  version.
  https://github.com/pgdg-packaging/pgdg-rpms/issues/16

* Sat Apr 19 2025 Devrim Gündüz <devrim@gunduz.org> - 1.4.2-43PGDG
- Rebuild on RHEL 8 because of an issue on the build instance

* Thu Apr 17 2025 Devrim Gündüz <devrim@gunduz.org> - 1.4.2-42PGDG
- Update to 1.4.2

* Wed Feb 21 2024 Devrim Gündüz <devrim@gunduz.org> - 1.2-11PGDG
- Add PGDG branding

* Thu Oct 1 2020 Devrim Gündüz <devrim@gunduz.org> - 1.2-10
- Initial packaging for the PostgreSQL RPM repository to satisfy Patroni
  dependency. Took the spec file from Fedora rawhide.
