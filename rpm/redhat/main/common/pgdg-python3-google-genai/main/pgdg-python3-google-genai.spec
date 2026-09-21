%global pypi_name google_genai

Name:		python-google-genai
Version:	1.0.0
Release:	1PGDG%{?dist}
Summary:	Google GenAI Python SDK

License:	Apache-2.0
URL:		https://github.com/googleapis/python-genai
Source0:	%{pypi_source %{pypi_name}}
# pyproject.toml has no build-backend key, so the pyproject macros treat this as a
# legacy project and look for a setup.py:
Patch0:		google-genai-add-build-backend.patch

BuildArch:	noarch
BuildRequires:	python3-devel pyproject-rpm-macros

%global _description %{expand:
Google Gen AI Python SDK provides an interface for developers to integrate
generative models of Google into their Python applications. It supports the
Gemini Developer API and Vertex AI APIs.}

%description %_description

%package -n python3-google-genai
Summary:	%{summary}

%description -n python3-google-genai %_description

%prep
%autosetup -p0 -n %{pypi_name}-%{version}

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files -l google

%check
%pyproject_check_import

%files -n python3-google-genai -f %{pyproject_files}
%doc README.md

%changelog
* Sun Sep 20 2026 Devrim Gündüz <devrim@gunduz.org> - 1.0.0-1PGDG
- Initial packaging for the PostgreSQL RPM repository to support pg_statviz
  package on RHEL 10, per:
  https://pypi.org/project/google-genai/1.0.0/
- 1.0.0 is the newest release with a source tarball that RHEL 10 can satisfy:
  later ones need typing-extensions 4.11 or newer.
- Add the missing build-backend key to pyproject.toml with a patch, as the
  pyproject macros otherwise look for a setup.py.
