%global pypi_name google_genai

%if 0%{?rhel} && 0%{?rhel} == 10
%global python3_pkgversion 3.12
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

Name:		python%{python3_pkgversion}-google-genai
# RHEL 10 (typing-extensions 4.9.0) stays on 1.0.0. Amazon Linux 2023 uses
# the newest release that works with google-auth 2.47 (2.48 and later need
# cryptography >= 38) and typing-extensions 4.12.2 (1.67.0 uses the
# extra_items argument of TypedDict, which needs 4.13), SLES 16 the newest one
# that works with its google-auth 2.38.
%if 0%{?rhel}
Version:	1.0.0
%endif
%if 0%{?amzn} == 2023
Version:	1.66.0
%endif
%if 0%{?suse_version}
Version:	1.55.0
%endif
Release:	2PGDG%{?dist}
Summary:	Google GenAI Python SDK

License:	Apache-2.0
URL:		https://github.com/googleapis/python-genai
Source0:	https://files.pythonhosted.org/packages/source/g/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
%if 0%{?rhel}
# pyproject.toml has no build-backend key, so the pyproject macros treat this as a
# legacy project and look for a setup.py:
Patch0:		google-genai-add-build-backend.patch
%endif

BuildArch:	noarch
BuildRequires:	python%{python3_pkgversion}-devel
%if 0%{?suse_version}
# The SUSE macros have no dynamic BuildRequires:
BuildRequires:	python-rpm-macros python%{python3_pkgversion}-pip
BuildRequires:	python%{python3_pkgversion}-setuptools python%{python3_pkgversion}-wheel
Requires:	python%{python3_pkgversion}-anyio python%{python3_pkgversion}-distro
Requires:	python%{python3_pkgversion}-google-auth python%{python3_pkgversion}-httpx
Requires:	python%{python3_pkgversion}-pydantic python%{python3_pkgversion}-requests
Requires:	python%{python3_pkgversion}-sniffio python%{python3_pkgversion}-tenacity
Requires:	python%{python3_pkgversion}-typing_extensions python%{python3_pkgversion}-websockets
%else
BuildRequires:	pyproject-rpm-macros
%endif

%description
Google Gen AI Python SDK provides an interface for developers to integrate
generative models of Google into their Python applications. It supports the
Gemini Developer API and Vertex AI APIs.

%prep
%autosetup -p0 -n %{pypi_name}-%{version}
%if ! 0%{?rhel}
# pyproject.toml has no build-backend key, so the pyproject macros treat this
# as a legacy project and look for a setup.py. twine, packaging and pkginfo
# are only needed for uploading to PyPI:
sed -i 's|^requires = \["setuptools", "wheel", "twine>=6.1.0", "packaging>=24.2", "pkginfo>=1.12.0"\]$|requires = ["setuptools", "wheel"]\nbuild-backend = "setuptools.build_meta"|' pyproject.toml
grep -q '^build-backend = "setuptools.build_meta"$' pyproject.toml
%endif
%if 0%{?amzn} == 2023
# The license metadata uses PEP 639, which needs setuptools >= 77. Use the
# older format, as Amazon Linux 2023 has setuptools 69:
sed -i 's|^license = "Apache-2.0"$|license = { text = "Apache-2.0" }|' pyproject.toml
grep -q '^license = { text = "Apache-2.0" }$' pyproject.toml
%endif

%if ! 0%{?suse_version}
%generate_buildrequires
%pyproject_buildrequires
%endif

%build
%pyproject_wheel

%install
%pyproject_install
%if ! 0%{?suse_version}
%pyproject_save_files -l google

%check
# google.genai.local_tokenizer needs the optional sentencepiece, the tests
# need pytest:
%pyproject_check_import -e 'google.genai.local_tokenizer' -e 'google.genai.tests' -e 'google.genai.tests.*'
%endif

%if 0%{?suse_version}
%files
%license LICENSE
%{python3_sitelib}/google/genai/
%{python3_sitelib}/%{pypi_name}-%{version}.dist-info/
%else
%files -f %{pyproject_files}
%endif
%doc README.md

%changelog
* Wed Oct 07 2026 Devrim Gunduz <devrim@gunduz.org> - 1.66.0-2PGDG
- Add Amazon Linux 2023 support with 1.66.0, and SLES 16 support with
  1.55.0, the newest releases that work with the dependencies there. Both
  for pg_statviz. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/249

* Sun Sep 20 2026 Devrim Gündüz <devrim@gunduz.org> - 1.0.0-1PGDG
- Initial packaging for the PostgreSQL RPM repository to support pg_statviz
  package on RHEL 10, per:
  https://pypi.org/project/google-genai/1.0.0/
- 1.0.0 is the newest release with a source tarball that RHEL 10 can satisfy:
  later ones need typing-extensions 4.11 or newer.
- Add the missing build-backend key to pyproject.toml with a patch, as the
  pyproject macros otherwise look for a setup.py.
