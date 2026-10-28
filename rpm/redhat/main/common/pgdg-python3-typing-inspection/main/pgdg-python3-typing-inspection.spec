%pgdg_python3_setup

%global	modname typing-inspection
%global	pymodname typing_inspection

Name:		python%{python3_pkgversion}-%{modname}
Version:	0.4.2
Release:	2PGDG%{?dist}
Summary:	Runtime typing introspection tools

License:	MIT
URL:		https://github.com/pydantic/%{modname}
Source0:	https://files.pythonhosted.org/packages/source/t/%{pymodname}/%{pymodname}-%{version}.tar.gz
BuildArch:	noarch

BuildRequires:	python%{python3_pkgversion}-devel
%if ! 0%{?suse_version}
BuildRequires:	pyproject-rpm-macros
%endif
BuildRequires:	python%{python3_pkgversion}-pip
BuildRequires:	python%{python3_pkgversion}-hatchling

Requires:	python%{python3_pkgversion}-typing-extensions >= 4.12.0

%description
typing-inspection provides tools to inspect type annotations at runtime.

%prep
%autosetup -n %{pymodname}-%{version}
%if 0%{?rhel} == 9
# The license-files array of PEP 639 needs hatchling 1.27, RHEL 9 has 1.25
# (1.27 needs packaging 24.2). The license file is still packaged below:
sed -i "/^license-files = \['LICENSE'\]$/d" pyproject.toml
if grep -q '^license-files' pyproject.toml; then exit 1; fi
%endif

%build
%pyproject_wheel

%install
%pyproject_install

%files
%license LICENSE
%doc README.md
%{python3_sitelib}/%{pymodname}/
%{python3_sitelib}/%{pymodname}-%{version}.dist-info/

%changelog
* Wed Oct 28 2026 Devrim Gunduz <devrim@gunduz.org> - 0.4.2-2PGDG
- Use %%pgdg_python3_setup from pgdg-srpm-macros 2.5.0 instead of the
  per-distro Python block and the __ospython macro. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/462

* Wed Oct 07 2026 Devrim Gunduz <devrim@gunduz.org> - 0.4.2-1PGDG
- Initial packaging for the PostgreSQL RPM repository, to satisfy
  pydantic dependency (for pg_statviz) on Amazon Linux 2023. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/249
- Add RHEL 9 support (python3.12), for pg_statviz. Drop the license-files
  key there, as hatchling 1.25 of RHEL 9 does not support its PEP 639 form.
  Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/249
