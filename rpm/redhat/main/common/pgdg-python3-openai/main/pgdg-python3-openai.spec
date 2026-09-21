%global pypi_name openai

Name:		python-%{pypi_name}
Version:	1.39.0
Release:	1PGDG%{?dist}
Summary:	The official Python library for the OpenAI API

License:	Apache-2.0
URL:		https://github.com/openai/openai-python
Source0:	%{pypi_source %{pypi_name}}
# httpx 0.28 (the one on RHEL 10) removed the proxies argument of httpx.Client,
# which this release still passes, so every OpenAI() call failed. The fix that
# upstream made in 1.55.3, that needs jiter, adapted to this release:
Patch0:		openai-httpx-0.28-proxies.patch

BuildArch:	noarch
BuildRequires:	python3-devel pyproject-rpm-macros

%description
The OpenAI Python library provides convenient access to the OpenAI REST API
from any Python 3.7+ application. The library includes type definitions for
all request params and response fields, and offers both synchronous and
asynchronous clients powered by httpx.

%package -n python3-%{pypi_name}
Summary:	%{summary}

%description -n python3-%{pypi_name} %_description

%prep
%autosetup -p0 -n %{pypi_name}-%{version}

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files %{pypi_name}

%check
# Only the import tests: the full test suite needs network access and API keys.
%pyproject_check_import

%files -n python3-%{pypi_name} -f %{pyproject_files}
%license LICENSE
%doc README.md CHANGELOG.md CONTRIBUTING.md
%{_bindir}/openai

%changelog
* Sun Sep 20 2026 Devrim Gündüz <devrim@gunduz.org> - 1.39.0-1PGDG
- Initial packaging for the PostgreSQL RPM repository to support pg_statviz
  package on RHEL 10, per:
  https://pypi.org/project/openai/1.39.0/
- 1.39.0 is the newest release that RHEL 10 can satisfy: later ones need jiter
  (a Rust extension), and typing-extensions 4.11 or newer.
- Add a patch for httpx 0.28: this release passes the removed proxies argument to
  httpx.Client, which made OpenAI() fail with "unexpected keyword argument
  'proxies'". Use the new proxy argument instead, as upstream did in 1.55.3.
