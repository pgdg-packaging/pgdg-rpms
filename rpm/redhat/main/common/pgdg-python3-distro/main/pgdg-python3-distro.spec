%pgdg_python3_setup

%global	modname distro
%global	pymodname distro

Name:		python%{python3_pkgversion}-%{modname}
Version:	1.9.0
Release:	2PGDG%{?dist}
Summary:	OS platform information API

License:	Apache-2.0
URL:		https://github.com/python-distro/%{modname}
Source0:	https://files.pythonhosted.org/packages/source/d/%{pymodname}/%{pymodname}-%{version}.tar.gz
BuildArch:	noarch

BuildRequires:	python%{python3_pkgversion}-devel
%if ! 0%{?suse_version}
BuildRequires:	pyproject-rpm-macros
%endif
BuildRequires:	python%{python3_pkgversion}-pip
BuildRequires:	python%{python3_pkgversion}-setuptools
BuildRequires:	python%{python3_pkgversion}-wheel

%description
distro provides information about the OS distribution it runs on, such as
a reliable machine-readable ID, or version information.

%prep
%autosetup -n %{pymodname}-%{version}

%build
%pyproject_wheel

%install
%pyproject_install
# Remove the command line tool, it conflicts with the python3-distro package
# of the OS:
%{__rm} -rf %{buildroot}%{_bindir}

%files
%license LICENSE
%doc README.md
%{python3_sitelib}/%{pymodname}/
%{python3_sitelib}/%{pymodname}-%{version}.dist-info/

%changelog
* Wed Oct 28 2026 Devrim Gunduz <devrim@gunduz.org> - 1.9.0-2PGDG
- Use %%pgdg_python3_setup from pgdg-srpm-macros 2.5.0 instead of the
  per-distro Python block and the __ospython macro. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/462

* Wed Oct 07 2026 Devrim Gunduz <devrim@gunduz.org> - 1.9.0-1PGDG
- Initial packaging for the PostgreSQL RPM repository, to satisfy
  anthropic dependency (for pg_statviz) on Amazon Linux 2023. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/249
- Add RHEL 9 support (python3.12), for pg_statviz. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/249
