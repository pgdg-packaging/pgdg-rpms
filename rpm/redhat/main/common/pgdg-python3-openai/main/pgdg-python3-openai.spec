%global pypi_name openai

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

# RHEL 10 (typing-extensions 4.9.0) and SLES 16 (no jiter) stay on 1.39.0.
# Amazon Linux 2023 uses the newest release that works with its
# typing-extensions 4.12.2 and anyio 4.9.0.
%if 0%{?amzn} == 2023
%global	oldsdk 0
%else
%global	oldsdk 1
%endif

Name:		python%{python3_pkgversion}-%{pypi_name}
%if %{oldsdk}
Version:	1.39.0
%else
Version:	2.28.0
%endif
Release:	2PGDG%{?dist}
Summary:	The official Python library for the OpenAI API

License:	Apache-2.0
URL:		https://github.com/openai/openai-python
Source0:	https://files.pythonhosted.org/packages/source/o/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
%if %{oldsdk}
# httpx 0.28 (the one on RHEL 10) removed the proxies argument of httpx.Client,
# which this release still passes, so every OpenAI() call failed. The fix that
# upstream made in 1.55.3, that needs jiter, adapted to this release:
Patch0:		openai-httpx-0.28-proxies.patch
%endif

BuildArch:	noarch
BuildRequires:	python%{python3_pkgversion}-devel
%if 0%{?suse_version}
# The SUSE macros have no dynamic BuildRequires:
BuildRequires:	python-rpm-macros python%{python3_pkgversion}-pip python%{python3_pkgversion}-wheel
BuildRequires:	python%{python3_pkgversion}-hatchling python%{python3_pkgversion}-hatch-fancy-pypi-readme
Requires:	python%{python3_pkgversion}-anyio python%{python3_pkgversion}-distro
Requires:	python%{python3_pkgversion}-httpx python%{python3_pkgversion}-pydantic
Requires:	python%{python3_pkgversion}-sniffio python%{python3_pkgversion}-tqdm
Requires:	python%{python3_pkgversion}-typing_extensions
%else
BuildRequires:	pyproject-rpm-macros
%endif

%description
The OpenAI Python library provides convenient access to the OpenAI REST API
from any Python 3.7+ application. The library includes type definitions for
all request params and response fields, and offers both synchronous and
asynchronous clients powered by httpx.

%prep
%autosetup -p0 -n %{pypi_name}-%{version}
%if ! %{oldsdk}
# The build needs exactly hatchling 1.26.3; any recent one works:
sed -i 's|^requires = \["hatchling==1.26.3", |requires = ["hatchling", |' pyproject.toml
grep -q '^requires = \["hatchling", ' pyproject.toml
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
%pyproject_save_files %{pypi_name}

%check
# Only the import tests: the full test suite needs network access and API keys.
# openai.helpers needs the voice_helpers extra (numpy, sounddevice).
%pyproject_check_import -e 'openai.helpers' -e 'openai.helpers.*'
%endif

%if 0%{?suse_version}
%files
%{python3_sitelib}/%{pypi_name}/
%{python3_sitelib}/%{pypi_name}-%{version}.dist-info/
%else
%files -f %{pyproject_files}
%endif
%license LICENSE
%doc README.md CHANGELOG.md CONTRIBUTING.md
%{_bindir}/openai

%changelog
* Wed Oct 07 2026 Devrim Gunduz <devrim@gunduz.org> - 1.39.0-2PGDG
- Add Amazon Linux 2023 support with 2.28.0, the newest release that works
  with typing-extensions 4.12.2 and anyio 4.9.0 there.
- Add SLES 16 support, with 1.39.0 and the httpx 0.28 patch, as SLES 16 has
  no jiter.
- Both for pg_statviz. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/249

* Sun Sep 20 2026 Devrim Gündüz <devrim@gunduz.org> - 1.39.0-1PGDG
- Initial packaging for the PostgreSQL RPM repository to support pg_statviz
  package on RHEL 10, per:
  https://pypi.org/project/openai/1.39.0/
- 1.39.0 is the newest release that RHEL 10 can satisfy: later ones need jiter
  (a Rust extension), and typing-extensions 4.11 or newer.
- Add a patch for httpx 0.28: this release passes the removed proxies argument to
  httpx.Client, which made OpenAI() fail with "unexpected keyword argument
  'proxies'". Use the new proxy argument instead, as upstream did in 1.55.3.
