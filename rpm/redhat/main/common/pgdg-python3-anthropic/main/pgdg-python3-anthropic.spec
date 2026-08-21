Name:		python-anthropic
Version:	1.0.0
Release:	1PGDG%{dist}
Summary:	The official Python library for the anthropic API

License:	MIT
URL:		https://github.com/anthropics/anthropic-sdk-python
Source:		%{pypi_source anthropic}
Patch:		python3-anthropic-relax-hatchling.patch

BuildArch:	noarch
BuildRequires:	python3-devel

BuildRequires:	python3-hatch-fancy-pypi-readme python3-mcp
BuildRequires:	python3-docstring-parser python3-google-auth+requests
BuildRequires:	python3-httpx2 python3-jiter


%description
The Claude SDK for Python provides access to the Claude API from Python applications.}

%package -n python3-anthropic
Summary:	The official Python library for the anthropic API

%description -n python3-anthropic
The Claude SDK for Python provides access to the Claude API from Python applications.}


%prep
%autosetup -p0 -n anthropic-%{version}

%generate_buildrequires
%pyproject_buildrequires -x aiohttp,bedrock,mcp,vertex

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files -l anthropic

%check
%pyproject_check_import

%files -n python3-anthropic -f %{pyproject_files}
%doc README.md CHANGELOG.md CONTRIBUTING.md SECURITY.md api.md helpers.md tools.md examples/
%license LICENSE

%changelog
* Fri Aug 21 2026 Devrim Gündüz <devrim@gunduz.org> - 1.0.0-1PGDG
- Initial packaging for PGDG RPM repository to support pg_statviz package, per:
  https://github.com/anthropics/anthropic-sdk-python/releases

