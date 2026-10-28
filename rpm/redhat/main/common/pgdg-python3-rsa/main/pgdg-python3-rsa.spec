%pgdg_python3_setup

%global	modname rsa
%global	pymodname rsa

Name:		python%{python3_pkgversion}-%{modname}
Version:	4.9.1
Release:	44PGDG%{?dist}
Summary:	Pure-Python RSA implementation

License:	Apache-2.0
URL:		https://github.com/sybrenstuvel/python-%{modname}
Source0:	https://files.pythonhosted.org/packages/source/r/%{pymodname}/%{pymodname}-%{version}.tar.gz
BuildArch:	noarch

BuildRequires:	python%{python3_pkgversion}-devel
%if ! 0%{?suse_version}
BuildRequires:	pyproject-rpm-macros
%endif
BuildRequires:	python%{python3_pkgversion}-pip
BuildRequires:	python%{python3_pkgversion}-poetry-core

Requires:	python%{python3_pkgversion}-pyasn1 >= 0.1.3

%if 0%{?rhel} == 10
# Replace the EPEL package of the same module, which has the same files:
Obsoletes:	python3-rsa < %{version}-%{release}
%endif

%description
Python-RSA is a pure-Python RSA implementation. It supports encryption and
decryption, signing and verifying signatures, and key generation.

%prep
%autosetup -n %{pymodname}-%{version}

%build
%pyproject_wheel

%install
%pyproject_install
%if 0%{?rhel} == 10
# Keep the command line tools, as EPEL's python3-rsa, which this package
# replaces, has them:
for f in %{buildroot}%{_bindir}/pyrsa-*; do
	%{__ln_s} $(basename $f) $f-3
done
%else
# Remove the command line tools, they conflict with the package of the OS
# Python:
%{__rm} -rf %{buildroot}%{_bindir}
%endif

%files
%license LICENSE
%doc README.md
%{python3_sitelib}/%{pymodname}/
%{python3_sitelib}/%{pymodname}-%{version}.dist-info/
%if 0%{?rhel} == 10
%{_bindir}/pyrsa-*
%endif

%changelog
* Wed Oct 28 2026 Devrim Gunduz <devrim@gunduz.org> - 4.9.1-44PGDG
- Use %%pgdg_python3_setup from pgdg-srpm-macros 2.5.0 instead of the
  per-distro Python block and the __ospython macro. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/462

* Mon Oct 26 2026 Devrim Gunduz <devrim@gunduz.org> - 4.9.1-43PGDG
- RHEL 10: Ship the pyrsa-* command line tools, as EPEL's python3-rsa,
  which this package replaces, does. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/422
* Sat Oct 24 2026 Devrim Gunduz <devrim@gunduz.org> - 4.9.1-42PGDG
- Add RHEL 10 support, without EPEL, and obsolete the EPEL python3-rsa
  package there. Start the release from 42, so that our packages win over
  EPEL's. Per https://github.com/pgdg-packaging/pgdg-rpms/issues/422

* Wed Oct 07 2026 Devrim Gunduz <devrim@gunduz.org> - 4.9.1-1PGDG
- Initial packaging for the PostgreSQL RPM repository, to satisfy
  google-auth dependency (for pg_statviz) on Amazon Linux 2023. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/249
- Add RHEL 9 support (python3.12), for pg_statviz. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/249
