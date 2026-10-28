%pgdg_python3_setup

%global	modname tqdm
%global	pymodname tqdm

Name:		python%{python3_pkgversion}-%{modname}
Version:	4.70.1
Release:	43PGDG%{?dist}
Summary:	Fast, extensible progress bar for Python

License:	MPL-2.0 AND MIT
URL:		https://github.com/tqdm/%{modname}
Source0:	https://files.pythonhosted.org/packages/source/t/%{pymodname}/%{pymodname}-%{version}.tar.gz
BuildArch:	noarch

BuildRequires:	python%{python3_pkgversion}-devel
%if ! 0%{?suse_version}
BuildRequires:	pyproject-rpm-macros
%endif
BuildRequires:	python%{python3_pkgversion}-pip
BuildRequires:	python%{python3_pkgversion}-setuptools
BuildRequires:	python%{python3_pkgversion}-wheel
BuildRequires:	python%{python3_pkgversion}-setuptools_scm

%if 0%{?rhel} == 10
# Replace the EPEL package of the same module, which has the same files:
Obsoletes:	python3-tqdm < %{version}-%{release}
%endif

%description
tqdm shows a smart progress meter for loops and iterables.

%prep
%autosetup -n %{pymodname}-%{version}

%build
%pyproject_wheel

%install
%pyproject_install
%if 0%{?rhel} == 10
# Keep the command line tool, as EPEL's python3-tqdm, which this package
# replaces, has it:
%{__install} -D -m 0644 tqdm/tqdm.1 %{buildroot}%{_mandir}/man1/tqdm.1
%else
# Remove the command line tools, they conflict with the package of the OS
# Python:
%{__rm} -rf %{buildroot}%{_bindir}
%endif

%files
%license LICENCE
%doc README.rst
%{python3_sitelib}/%{pymodname}/
%{python3_sitelib}/%{pymodname}-%{version}.dist-info/
%if 0%{?rhel} == 10
%{_bindir}/tqdm
%{_mandir}/man1/tqdm.1*
%endif

%changelog
* Wed Oct 28 2026 Devrim Gunduz <devrim@gunduz.org> - 4.70.1-43PGDG
- Use %%pgdg_python3_setup from pgdg-srpm-macros 2.5.0 instead of the
  per-distro Python block and the __ospython macro. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/462

* Tue Oct 27 2026 Devrim Gunduz <devrim@gunduz.org> - 4.70.1-42PGDG
- Update to 4.70.1, per changes described at:
  https://github.com/tqdm/tqdm/releases/tag/v4.70.1
  On RHEL 10, EPEL has 4.68.4, and its python3-tqdm obsoletes
  python3.12-tqdm < 4.68.4, which replaced ours. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/422

* Mon Oct 26 2026 Devrim Gunduz <devrim@gunduz.org> - 4.67.1-43PGDG
- RHEL 10: Ship the tqdm command line tool and its man page, as EPEL's
  python3-tqdm, which this package replaces, does. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/422
* Sat Oct 24 2026 Devrim Gunduz <devrim@gunduz.org> - 4.67.1-42PGDG
- Add RHEL 10 support, without EPEL, and obsolete the EPEL python3-tqdm
  package there. Start the release from 42, so that our packages win over
  EPEL's. Per https://github.com/pgdg-packaging/pgdg-rpms/issues/422

* Wed Oct 07 2026 Devrim Gunduz <devrim@gunduz.org> - 4.67.1-1PGDG
- Initial packaging for the PostgreSQL RPM repository, to satisfy
  openai dependency (for pg_statviz) on Amazon Linux 2023. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/249
- Add RHEL 9 support (python3.12), for pg_statviz. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/249
