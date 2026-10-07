%global pypi_name ollama

%if 0%{?rhel} && 0%{?rhel} == 10
%global python3_pkgversion 3.12
%endif
%if 0%{?rhel} == 9
%global	__ospython %{_bindir}/python3.12
%global	__python3 %{_bindir}/python3.12
%global	python3_pkgversion 3.12
%endif
%if 0%{?amzn} == 2023
%global	__ospython %{_bindir}/python3.13
%global	__python3 %{_bindir}/python3.13
%global	python3_pkgversion 3.13
%endif
%if 0%{?suse_version} == 1600
%global	__ospython %{_bindir}/python3.13
%global	python3_pkgversion 313
%endif

Name:		python%{python3_pkgversion}-%{pypi_name}
Version:	0.6.2
Release:	2PGDG%{?dist}
Summary:	The official Python client for Ollama

License:	MIT
URL:		https://ollama.com
Source0:	https://files.pythonhosted.org/packages/source/o/%{pypi_name}/%{pypi_name}-%{version}.tar.gz

BuildArch:	noarch
BuildRequires:	python%{python3_pkgversion}-devel
%if 0%{?suse_version}
# The SUSE macros have no dynamic BuildRequires:
BuildRequires:	python-rpm-macros python%{python3_pkgversion}-pip python%{python3_pkgversion}-wheel
BuildRequires:	python%{python3_pkgversion}-hatchling python%{python3_pkgversion}-hatch_vcs
Requires:	python%{python3_pkgversion}-httpx >= 0.27
Requires:	python%{python3_pkgversion}-pydantic >= 2.9
%else
BuildRequires:	pyproject-rpm-macros
%endif

%description
The Ollama Python library provides the easiest way to integrate Python 3.8+
projects with Ollama.

%prep
%autosetup -n %{pypi_name}-%{version}

%if ! 0%{?suse_version}
%generate_buildrequires
%pyproject_buildrequires
%endif

%build
%pyproject_wheel

%install
%pyproject_install
%if ! 0%{?suse_version}
%pyproject_save_files %{pypi_name}

%check
%pyproject_check_import
%endif

%if 0%{?suse_version}
%files
%{python3_sitelib}/%{pypi_name}/
%{python3_sitelib}/%{pypi_name}-%{version}.dist-info/
%else
%files -f %{pyproject_files}
%endif
%license LICENSE
%doc README.md

%changelog
* Wed Oct 07 2026 Devrim Gunduz <devrim@gunduz.org> - 0.6.2-2PGDG
- Add Amazon Linux 2023 support (python3.13), for pg_statviz.
- Add RHEL 9 support (python3.12), for pg_statviz.
- Add SLES 16 support, for pg_statviz: the python313-ollama 0.4.7 of SLES 16
  has no "think" argument in chat(), which pg_statviz uses. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/249

* Sun Sep 20 2026 Devrim Gündüz <devrim@gunduz.org> - 0.6.2-1PGDG
- Initial packaging for the PostgreSQL RPM repository to support pg_statviz
  package on RHEL 10, per:
  https://pypi.org/project/ollama/0.6.2/
