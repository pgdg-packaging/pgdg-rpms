%if 0%{?fedora} && 0%{?fedora} == 43
%global __ospython %{_bindir}/python3.14
%global python3_pkgversion 3.14
%endif
%if 0%{?fedora} && 0%{?fedora} <= 42
%global	__python3 %{_bindir}/python3.13
%global	python3_pkgversion 3.13
%endif
%if 0%{?rhel} && 0%{?rhel} <= 10
%global	__python3 %{_bindir}/python3.12
%global	python3_pkgversion 3.12
%endif
%if 0%{?suse_version} >= 1500
%global	__python3 %{_bindir}/python3.11
%global	python3_pkgversion 311
%endif

Name:		python%{python3_pkgversion}-dns
Version:	1.15.0
Release:	42PGDG%{?dist}.1
Summary:	DNS toolkit for Python

Group:		Development/Languages
License:	MIT
URL:		http://www.dnspython.org/

Source0:	http://www.dnspython.org/kits/%{version}/dnspython-%{version}.tar.gz

BuildArch:	noarch

BuildRequires:	python%{python3_pkgversion}-devel
BuildRequires:	python%{python3_pkgversion}-setuptools

%description
dnspython is a DNS toolkit for Python. It supports almost all record
types. It can be used for queries, zone transfers, and dynamic
updates. It supports TSIG authenticated messages and EDNS0.

dnspython provides both high and low level access to DNS. The high
level classes perform queries for data of a given name, type, and
class, and return an answer set. The low level classes allow direct
manipulation of DNS zones, messages, names, and records.

%prep
%setup -q -n dnspython-%{version}

# strip exec permissions so that we don't pick up dependencies from docs
find examples -type f | xargs chmod a-x

%build
%py3_build

%install
%py3_install
%files -n python%{python3_pkgversion}-dns
%defattr(-,root,root,-)
# Add README.* when it is included with the source (commit a906279)
%doc {ChangeLog,LICENSE,examples}
%{python3_sitelib}/*egg-info
%{python3_sitelib}/dns

%changelog
* Mon Sep 22 2025 Devrim Gunduz <devrim@gunduz.org> - 1.15.0-42PGDG.1
- Add Fedora 43 support

* Wed May 21 2025 Devrim Gunduz <devrim@gunduz.org> - 1.15.0-42PGDG
- Initial packaging for the PostgreSQL RPM repository to support
  patroni-etcd package on RHEL 9.
