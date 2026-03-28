%global modname daemonize

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

Name:		python%{python3_pkgversion}-%{modname}
Version:	2.5.0
Release:	42%{?dist}
Summary:	Library for writing system daemons in Python

License:	MIT
URL:		https://github.com/thesharp/%{modname}
Source0:	%{url}/archive/v%{version}/%{modname}-%{version}.tar.gz

BuildArch:	noarch

BuildRequires:	python%{python3_pkgversion}-devel

%description
daemonize is a library for writing system daemons in Python.

%prep
%autosetup -n %{modname}-%{version}

%build
%py3_build

%install
%py3_install

%files
%license LICENSE
%doc README.rst
%{python3_sitelib}/%{modname}-*.egg-info/
%{python3_sitelib}/%{modname}.py
%if 0%{?fedora} >= 41 || 0%{?rhel} >= 9
%{python3_sitelib}/__pycache__/%{modname}.*
%endif

%changelog
* Sat Mar 28 2026 Devrim Gündüz <devrim@gunduz.org> - 2.5.0-42
- Add to SLES

* Thu Dec 10 2020 Devrim Gündüz <devrim@gunduz.org> - 2.5.0-8
- Initial packaging to satisfy pg_chameleon dependency on
  RHEL 7 and 8.
