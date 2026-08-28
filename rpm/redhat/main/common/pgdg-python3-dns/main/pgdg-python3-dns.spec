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

Name:		python%{python3_pkgversion}-dns
Version:	2.8.0
Release:	48PGDG%{?dist}
Summary:	DNS toolkit for Python

Group:		Development/Languages
License:	MIT
URL:		http://www.dnspython.org/

Source0:	https://github.com/rthalley/dnspython/releases/download/v%{version}/dnspython-%{version}.tar.gz
Patch0:		pgdg-python3-dns-removehatchling.patch

BuildArch:	noarch

BuildRequires:	python%{python3_pkgversion}-devel

Provides:	python3-%{sname}%{?_isa} = %{version}-%{release}
Provides:	python%{python3_pkgversion}dist(dnspython) = %{version}-%{release}

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
%patch -P 0 -p0

# strip exec permissions so that we don't pick up dependencies from docs
find examples -type f | xargs chmod a-x

%build
%pyproject_wheel

%install
%pyproject_install

%files -n python%{python3_pkgversion}-dns
%defattr(-,root,root,-)
# Add README.* when it is included with the source (commit a906279)
%doc {ChangeLog,LICENSE,examples}
%{python3_sitelib}/dnspython-*.dist-info/
%{python3_sitelib}/dns

%changelog
* Fri Aug 28 2026 Devrim Gunduz <devrim@gunduz.org> - 2.8.0-48PGDG
- Package the .dist-info directory itself instead of globbing only its
  contents (dist-info/*), so RHEL/Fedora's pythondist.attr generator
  (which is anchored on the .dist-info directory entry) actually fires
  and emits the correct runtime Requires. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/226

* Tue Aug 25 2026 Devrim Gunduz <devrim@gunduz.org> - 2.8.0-47PGDG
- Also set __python3 (not just __ospython) for Amazon Linux 2023, so
  %pyproject_wheel/%pyproject_install actually build against python3.13
  instead of silently falling back to the system default python3
  (__ospython only affects this repo's own macro computations, not
  RPM's own pyproject/site-packages macros).

* Tue Aug 25 2026 Devrim Gunduz <devrim@gunduz.org> - 2.8.0-46PGDG
- Build against the python3.13 alt-stack on Amazon Linux 2023, to keep
  the Python stack consistent across all packages in the repo.

* Wed May 6 2026 Devrim Gunduz <devrim@gunduz.org> - 2.8.0-45PGDG
- Fix Provides so that it provides the correct package name. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/190

* Mon May 4 2026 Devrim Gunduz <devrim@gunduz.org> - 2.8.0-44PGDG
- Use Python 3.14 on Fedora 44. Many BRs and Requires are not ready for 3.15.
  Per #167.
- Fix https://github.com/pgdg-packaging/pgdg-rpms/issues/180

* Thu Apr 9 2026 Devrim Gunduz <devrim@gunduz.org> - 2.8.0-43PGDG
- Fix a dependency issue

* Thu Apr 9 2026 Devrim Gunduz <devrim@gunduz.org> - 2.8.0-42PGDG
- Update to 2.8.0, per:
  https://github.com/pgdg-packaging/pgdg-rpms/issues/180
- Add Fedora 44 support

* Mon Sep 22 2025 Devrim Gunduz <devrim@gunduz.org> - 1.15.0-42PGDG.1
- Add Fedora 43 support

* Wed May 21 2025 Devrim Gunduz <devrim@gunduz.org> - 1.15.0-42PGDG
- Initial packaging for the PostgreSQL RPM repository to support
  patroni-etcd package on RHEL 9.
