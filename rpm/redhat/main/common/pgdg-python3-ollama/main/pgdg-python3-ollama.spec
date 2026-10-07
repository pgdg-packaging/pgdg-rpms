%global pypi_name ollama

%if 0%{?rhel} && 0%{?rhel} == 10
%global python3_pkgversion 3.12
%endif
%if 0%{?amzn} == 2023
%global	__ospython %{_bindir}/python3.13
%global	__python3 %{_bindir}/python3.13
%global	python3_pkgversion 3.13
%endif

Name:		python%{python3_pkgversion}-%{pypi_name}
Version:	0.6.2
Release:	2PGDG%{?dist}
Summary:	The official Python client for Ollama

License:	MIT
URL:		https://ollama.com
Source0:	%{pypi_source %{pypi_name}}

BuildArch:	noarch
BuildRequires:	python%{python3_pkgversion}-devel pyproject-rpm-macros

%description
The Ollama Python library provides the easiest way to integrate Python 3.8+
projects with Ollama.

%prep
%autosetup -n %{pypi_name}-%{version}

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files %{pypi_name}

%check
%pyproject_check_import

%files -f %{pyproject_files}
%license LICENSE
%doc README.md

%changelog
* Wed Oct 07 2026 Devrim Gunduz <devrim@gunduz.org> - 0.6.2-2PGDG
- Add Amazon Linux 2023 support (python3.13), for pg_statviz. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/249

* Sun Sep 20 2026 Devrim Gündüz <devrim@gunduz.org> - 0.6.2-1PGDG
- Initial packaging for the PostgreSQL RPM repository to support pg_statviz
  package on RHEL 10, per:
  https://pypi.org/project/ollama/0.6.2/
