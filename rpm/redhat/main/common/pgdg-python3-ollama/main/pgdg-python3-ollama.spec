%global pypi_name ollama

Name:		python-%{pypi_name}
Version:	0.6.2
Release:	1PGDG%{?dist}
Summary:	The official Python client for Ollama

License:	MIT
URL:		https://ollama.com
Source0:	%{pypi_source %{pypi_name}}

BuildArch:	noarch
BuildRequires:	python3-devel pyproject-rpm-macros

%global _description %{expand:
The Ollama Python library provides the easiest way to integrate Python 3.8+
projects with Ollama.}

%description %_description

%package -n python3-%{pypi_name}
Summary:	%{summary}

%description -n python3-%{pypi_name} %_description

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

%files -n python3-%{pypi_name} -f %{pyproject_files}
%license LICENSE
%doc README.md

%changelog
* Sun Sep 20 2026 Devrim Gündüz <devrim@gunduz.org> - 0.6.2-1PGDG
- Initial packaging for the PostgreSQL RPM repository to support pg_statviz
  package on RHEL 10, per:
  https://pypi.org/project/ollama/0.6.2/
