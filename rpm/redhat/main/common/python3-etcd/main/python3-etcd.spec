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

%global modname etcd
%global srcname python-%{modname}

%{expand: %%global py3ver %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:4])"`)}
%global python3_sitelib %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")

Name:		python%{python3_pkgversion}-%{modname}
Version:	0.4.5
Release:	48PGDG%{?dist}
Summary:	A python client library for etcd

License:	MIT
URL:		http://pypi.python.org/pypi/%{srcname}
# Using the github URL because the tarball file at pypi excludes
# the license file. But github tarball files are named awkwardly.
Source0:	https://github.com/jplana/%{srcname}/archive/%{version}.tar.gz

BuildArch:	noarch

# See https://bugzilla.redhat.com/1393497
# Also https://fedoraproject.org/wiki/Packaging:Guidelines#Noarch_with_Unported_Dependencies
ExclusiveArch:	noarch %{ix86} x86_64 %{arm} aarch64 ppc64le s390x powerpc64le

%if 0%{?fedora} && 0%{?fedora} >= 41
Requires:	python3-urllib3 >= 1.7.1
Requires:	python3-dns >= 1.13.0
%endif

%if 0%{?rhel} && 0%{?rhel} >= 10
Requires:	python3-urllib3 >= 1.7.1
Requires:	python3-dns >= 1.13.0
%endif

%if 0%{?rhel} && 0%{?rhel} <= 9
Requires:	python%{python3_pkgversion}-urllib3 >= 1.7.1
Requires:	python%{python3_pkgversion}-dns >= 1.13.0
%endif

%if 0%{?suse_version}
%if 0%{?suse_version} >= 1315
Requires:	python%{python3_pkgversion}-urllib3 >= 1.7.1
Requires:	python%{python3_pkgversion}-dnspython >= 1.13.0
%endif
%endif

%description
Client library for interacting with an etcd service, providing Python
access to the full etcd REST API. Includes authentication, accessing
and manipulating shared content, managing cluster members, and leader
election.

%prep
%autosetup -p1 -n %{srcname}-%{version}

%build
%{__ospython} setup.py build

%install
%{__rm} -rf %{buildroot}
%{__ospython} setup.py install --root %{buildroot} -O1 --skip-build

%files
%doc README.rst
%license LICENSE.txt
%{python3_sitelib}/*

%changelog
* Wed May 21 2025 Devrim Gündüz <devrim@gunduz.org> - 0.4.5-48PGDG
- Fix conditionals around dependency definitions.

* Wed May 21 2025 Devrim Gündüz <devrim@gunduz.org> - 0.4.5-47PGDG
- Rebuild against Python 3.12 on RHEL 8 and 9 and Python 3.11 on SLES 15.

* Wed Jan 10 2024 Devrim Gündüz <devrim@gunduz.org> - 0.4.5-46PGDG
- Remove RHEL 7 support
- Add PGDG branding

* Wed Jan 10 2024 Devrim Gündüz <devrim@gunduz.org> - 0.4.5-45
- Add explicit dependencies for RHEL >= 8

* Fri Jun 2 2023 Devrim Gündüz <devrim@gunduz.org> - 0.4.5-44
- Add SLES 15 support.

* Thu Mar 23 2023 Devrim Gündüz <devrim@gunduz.org> - 0.4.5-43
- Fix a dependency name

* Wed Sep 21 2022 Devrim Gündüz <devrim@gunduz.org> - 0.4.5-42
- Fix dependencies. The previous one was for tests. Now we specify
  runtime dependencies.

* Wed Aug 5 2020 Devrim Gündüz <devrim@gunduz.org> - 0.4.5-20
- Initial packaging for PostgreSQL RPM repository to satisfy
  patroni dependency on RHEL 8
