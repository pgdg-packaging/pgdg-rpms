%if 0%{?amzn} == 2023
%global	__ospython %{_bindir}/python3.13
%global	__python3 %{_bindir}/python3.13
%global	python3_pkgversion 3.13
%endif

# Newer releases need typing-extensions >= 4.10 (RHEL 10 has 4.9.0, AL2023 has
# 4.12.2 for python3.13) and httpx2, which are not available there. pg_statviz
# only uses the Messages API, which 0.40.0 supports.
%if 0%{?rhel} == 10 || 0%{?amzn} == 2023
%global	oldsdk 1
%else
%global	oldsdk 0
%endif

Name:		python-anthropic
%if %{oldsdk}
Version:	0.40.0
%else
Version:	1.11.0
%endif
Release:	1PGDG%{dist}
Summary:	The official Python library for the anthropic API

License:	MIT
URL:		https://github.com/anthropics/anthropic-sdk-python
Source:		%{pypi_source anthropic}
%if ! %{oldsdk}
Patch:		python3-anthropic-relax-hatchling.patch
%endif

BuildArch:	noarch
BuildRequires:	python%{python3_pkgversion}-devel

%if %{oldsdk}
BuildRequires:	pyproject-rpm-macros
%else
BuildRequires:	python3-hatch-fancy-pypi-readme python3-mcp
BuildRequires:	python3-docstring-parser python3-google-auth+requests
BuildRequires:	python3-httpx2 python3-jiter python3-sniffio
BuildRequires:	python3-aiohttp python3-boto3 python3-botocore
%endif


%description
The Claude SDK for Python provides access to the Claude API from Python applications.

%package -n python%{python3_pkgversion}-anthropic
Summary:	The official Python library for the anthropic API

%description -n python%{python3_pkgversion}-anthropic
The Claude SDK for Python provides access to the Claude API from Python applications.


%prep
%autosetup -p0 -n anthropic-%{version}

%generate_buildrequires
%if %{oldsdk}
%pyproject_buildrequires
%else
%pyproject_buildrequires -x aiohttp,bedrock,mcp,vertex
%endif

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files -l anthropic

%check
%if %{oldsdk}
# Without the bedrock and vertex extras, only check the top-level modules:
%pyproject_check_import -t
%else
%pyproject_check_import
%endif

%files -n python%{python3_pkgversion}-anthropic -f %{pyproject_files}
%if %{oldsdk}
%doc README.md CHANGELOG.md CONTRIBUTING.md SECURITY.md api.md helpers.md
%else
%doc README.md CHANGELOG.md CONTRIBUTING.md SECURITY.md api.md helpers.md tools.md examples/
%endif
%license LICENSE

%changelog
* Wed Oct 07 2026 Devrim Gunduz <devrim@gunduz.org> - 1.11.0-1PGDG
- Add RHEL 10 and Amazon Linux 2023 support for pg_statviz. Use 0.40.0
  there, without the extras: newer releases need typing-extensions >= 4.10
  and httpx2. Fedora stays on 1.11.0. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/249

* Fri Oct 2 2026 Devrim Gündüz <devrim@gunduz.org> - 1.11.0-1PGDG
- Update to 1.11.0 per changes described at:
  https://github.com/anthropics/anthropic-sdk-python/releases#release-v1.11.0
  https://github.com/anthropics/anthropic-sdk-python/releases#release-v1.10.0
  https://github.com/anthropics/anthropic-sdk-python/releases#release-v1.9.0
  https://github.com/anthropics/anthropic-sdk-python/releases#release-v1.8.0

* Sun Sep 20 2026 Devrim Gündüz <devrim@gunduz.org> - 1.7.0-1PGDG
- Update to 1.7.0 per changes described at:
  https://github.com/anthropics/anthropic-sdk-python/releases#release-v1.7.0
  https://github.com/anthropics/anthropic-sdk-python/releases#release-v1.6.0
  https://github.com/anthropics/anthropic-sdk-python/releases#release-v1.5.0

* Sat Sep 5 2026 Devrim Gündüz <devrim@gunduz.org> - 1.4.0-1PGDG
- Update to 1.4.0 per changes described at:
  https://github.com/anthropics/anthropic-sdk-python/releases#release-v1.4.0
  https://github.com/anthropics/anthropic-sdk-python/releases#release-v1.3.0

* Mon Aug 31 2026 Devrim Gündüz <devrim@gunduz.org> - 1.2.0-1PGDG
- Update to 1.2.0 per changes described at:
  https://pypi.org/project/anthropic/1.2.0/

* Fri Aug 21 2026 Devrim Gündüz <devrim@gunduz.org> - 1.0.0-1PGDG
- Initial packaging for PGDG RPM repository to support pg_statviz package, per:
  https://github.com/anthropics/anthropic-sdk-python/releases

