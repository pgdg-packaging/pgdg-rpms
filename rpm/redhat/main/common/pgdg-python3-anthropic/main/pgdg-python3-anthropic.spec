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

# Newer releases need typing-extensions >= 4.10 (RHEL 10 has 4.9.0, AL2023 has
# 4.12.2 for python3.13; 0.86 and later need >= 4.14, SLES 16 has 4.13.2) and
# httpx2, which are not available there. pg_statviz only uses the Messages
# API, which 0.40.0 supports.
%if 0%{?rhel} == 9 || 0%{?rhel} == 10 || 0%{?amzn} == 2023 || 0%{?suse_version} == 1600
%global	oldsdk 1
%else
%global	oldsdk 0
%endif

%if 0%{?suse_version}
# SUSE only generates runtime Requires from the Python metadata when asked
# to; Fedora and RHEL do it by default.
%{?python_enable_dependency_generator}
%endif

Name:		python%{python3_pkgversion}-anthropic
%if %{oldsdk}
Version:	0.40.0
Release:	3PGDG%{dist}
%else
Version:	2.3.0
Release:	1PGDG%{dist}
%endif
Summary:	The official Python library for the anthropic API

# 2.0.0 and later are Apache-2.0; code from before the change stays MIT:
%if %{oldsdk}
License:	MIT
%else
License:	Apache-2.0 AND MIT
%endif
URL:		https://github.com/anthropics/anthropic-sdk-python
Source:		https://files.pythonhosted.org/packages/source/a/anthropic/anthropic-%{version}.tar.gz
%if ! %{oldsdk}
Patch:		python3-anthropic-relax-hatchling.patch
%endif

BuildArch:	noarch
BuildRequires:	python%{python3_pkgversion}-devel

%if %{oldsdk}
%if 0%{?suse_version}
# The SUSE macros have no dynamic BuildRequires:
BuildRequires:	python-rpm-macros python%{python3_pkgversion}-pip python%{python3_pkgversion}-wheel
BuildRequires:	python%{python3_pkgversion}-hatchling python%{python3_pkgversion}-hatch-fancy-pypi-readme
%if 0%{?suse_version} >= 1600
# SUSE's Python dependency generators. python3-devel pulls this in, but
# python%%{python3_pkgversion}-devel does not.
BuildRequires:	python-rpm-packaging
%endif
%else
BuildRequires:	pyproject-rpm-macros
%endif
%else
BuildRequires:	python3-hatch-fancy-pypi-readme python3-mcp
BuildRequires:	python3-docstring-parser python3-google-auth+requests
BuildRequires:	python3-httpx2 python3-jiter python3-sniffio
BuildRequires:	python3-aiohttp python3-boto3 python3-botocore
BuildRequires:	python3-opentelemetry-api
%endif

%description
The Claude SDK for Python provides access to the Claude API from Python applications.

%prep
%autosetup -p0 -n anthropic-%{version}

%if ! 0%{?suse_version}
%generate_buildrequires
%if %{oldsdk}
%pyproject_buildrequires
%else
%pyproject_buildrequires -x aiohttp,bedrock,mcp,vertex
%endif
%endif

%build
%pyproject_wheel

%install
%pyproject_install
%if ! 0%{?suse_version}
%pyproject_save_files -l anthropic

%check
%if %{oldsdk}
# Without the bedrock and vertex extras, only check the top-level modules:
%pyproject_check_import -t
%else
%pyproject_check_import
%endif
%endif

%if 0%{?suse_version}
%files -n python%{python3_pkgversion}-anthropic
%{python3_sitelib}/anthropic/
%{python3_sitelib}/anthropic-%{version}.dist-info/
%else
%files -n python%{python3_pkgversion}-anthropic -f %{pyproject_files}
%endif
%if %{oldsdk}
%doc README.md CHANGELOG.md CONTRIBUTING.md SECURITY.md api.md helpers.md
%else
%doc README.md CHANGELOG.md CONTRIBUTING.md SECURITY.md api.md helpers.md tools.md examples/
%endif
%license LICENSE
%if ! %{oldsdk}
%license LICENSE-MIT
%endif

%changelog
* Mon Oct 26 2026 Devrim Gunduz <devrim@gunduz.org> - 0.40.0-3PGDG
- SLES 16: Generate the runtime Requires from the Python metadata, and
  BuildRequire python-rpm-packaging for the Python dependency generators.
  The package did not require anyio, distro, httpx, jiter, pydantic, sniffio and typing-extensions there, so it could not be
  imported. Per https://github.com/pgdg-packaging/pgdg-rpms/issues/427

* Sat Oct 24 2026 Devrim Gunduz <devrim@gunduz.org> - 2.3.0-1PGDG
- Update to 2.3.0 on Fedora, per changes described at:
  https://github.com/anthropics/anthropic-sdk-python/releases/tag/v2.3.0
  https://github.com/anthropics/anthropic-sdk-python/releases/tag/v2.2.0
  Per https://github.com/pgdg-packaging/pgdg-rpms/issues/445

* Thu Oct 22 2026 Devrim Gunduz <devrim@gunduz.org> - 2.1.0-1PGDG
- Update to 2.1.0 on Fedora, per changes described at:
  https://github.com/anthropics/anthropic-sdk-python/releases/tag/v2.1.0
  https://github.com/anthropics/anthropic-sdk-python/releases/tag/v2.0.0
  2.0.0 switched to API version 2026-10-21 and sends the API key in the
  Authorization header; pg_statviz only calls messages.create() with a
  top-level system prompt and one user message, which 2.x still accepts. The license is now Apache-2.0, with the code from
  before the change under MIT (LICENSE-MIT).
  Per https://github.com/pgdg-packaging/pgdg-rpms/issues/426

* Wed Oct 21 2026 Devrim Gunduz <devrim@gunduz.org> - 1.17.0-1PGDG
- Update to 1.17.0 on Fedora, per changes described at:
  https://github.com/anthropics/anthropic-sdk-python/releases/tag/v1.17.0
  Per https://github.com/pgdg-packaging/pgdg-rpms/issues/417

* Fri Oct 16 2026 Devrim Gunduz <devrim@gunduz.org> - 1.15.0-1PGDG
- Update to 1.15.0 on Fedora, per changes described at:
  https://github.com/anthropics/anthropic-sdk-python/releases/tag/v1.15.0
  Per https://github.com/pgdg-packaging/pgdg-rpms/issues/394

* Wed Oct 14 2026 Devrim Gunduz <devrim@gunduz.org> - 1.14.0-1PGDG
- Update to 1.14.0 on Fedora, per changes described at:
  https://github.com/anthropics/anthropic-sdk-python/releases/tag/v1.14.0
  It needs python3-opentelemetry-api, which Fedora provides.
  Per https://github.com/pgdg-packaging/pgdg-rpms/issues/381

* Fri Oct 09 2026 Devrim Gunduz <devrim@gunduz.org> - 1.13.0-1PGDG
- Update to 1.13.0 on Fedora, per changes described at:
  https://github.com/anthropics/anthropic-sdk-python/releases/tag/v1.13.0
  Per https://github.com/pgdg-packaging/pgdg-rpms/issues/350

* Thu Oct 08 2026 Devrim Gunduz <devrim@gunduz.org> - 1.12.1-2PGDG
- Update package name so that it matches our other Python packages.

* Thu Oct 08 2026 Devrim Gunduz <devrim@gunduz.org> - 1.12.1-1PGDG
- Update to 1.12.1 per changes described at:
  https://github.com/anthropics/anthropic-sdk-python/releases#release-v1.12.1
  RHEL 9, RHEL 10, Amazon Linux 2023 and SLES 16 stay on 0.40.0.

* Wed Oct 07 2026 Devrim Gunduz <devrim@gunduz.org> - 1.12.0-1PGDG
- Update to 1.12.0 per changes described at:
  https://github.com/anthropics/anthropic-sdk-python/releases#release-v1.12.0
  RHEL 9, RHEL 10, Amazon Linux 2023 and SLES 16 stay on 0.40.0.

* Wed Oct 07 2026 Devrim Gunduz <devrim@gunduz.org> - 1.11.0-1PGDG
- Add RHEL 9, RHEL 10, Amazon Linux 2023 and SLES 16 support for pg_statviz. Use
  0.40.0 there, without the extras: newer releases need typing-extensions >= 4.10
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

