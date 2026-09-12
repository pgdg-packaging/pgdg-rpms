%global pypi_name attrs
%global sname attr
%if 0%{?fedora} && 0%{?fedora} == 45
%global __ospython %{_bindir}/python3.15
%global python3_pkgversion 3.15
%endif
%if 0%{?fedora} && 0%{?fedora} <= 44
%global __ospython %{_bindir}/python3.14
%global python3_pkgversion 3.14
%endif
%if 0%{?rhel} && 0%{?rhel} <= 10
%global	__ospython %{_bindir}/python3.12
%global	python3_pkgversion 3.12
%endif
%if 0%{?amzn} == 2023
%global	__ospython %{_bindir}/python3.13
%global	python3_pkgversion 3.13
%endif
%if 0%{?suse_version} == 1500
%global	__ospython %{_bindir}/python3.11
%global	python3_pkgversion 311
%endif
%if 0%{?suse_version} == 1600
%global	__ospython %{_bindir}/python3.13
%global	python3_pkgversion 313
%endif
%{expand: %%global pyver %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:4])"`)}
%global python3_sitelib %(%{__ospython} -Esc "import sysconfig; print(sysconfig.get_path('purelib', vars={'platbase': '/usr', 'base': '%{_prefix}'}))")

Name:		python%{python3_pkgversion}-attrs
Version:	26.1.0
Release:	2PGDG%{?dist}
Summary:	Python attributes without boilerplate

License:	MIT
URL:		https://www.attrs.org/
BuildArch:	noarch
Source0:	https://github.com/python-attrs/%{pypi_name}/archive/refs/tags/%{version}.tar.gz

BuildRequires:	python%{python3_pkgversion}-devel python%{python3_pkgversion}-pip
BuildRequires:	python%{python3_pkgversion}-hatchling python%{python3_pkgversion}-hatch-vcs
BuildRequires:	python%{python3_pkgversion}-hatch-fancy-pypi-readme
%if 0%{?suse_version} >= 1500
BuildRequires:	python-rpm-macros
%else
BuildRequires:	pyproject-rpm-macros
%endif
Requires:	python%{python3_pkgversion}


%description
attrs is an MIT-licensed Python package with class decorators that
ease the chores of implementing the most common attribute-related
object protocols.

%prep
%setup -q -n %{pypi_name}-%{version}

%build
%pyproject_wheel

%install
%pyproject_install

%files
%license LICENSE
%doc README.md
%{python3_sitelib}/%{pypi_name}-%{version}.dist-info/
%{python3_sitelib}/%{sname}/*.py*
%{python3_sitelib}/%{sname}/py.typed
%{python3_sitelib}/%{sname}/__pycache__/*.pyc
%{python3_sitelib}/%{pypi_name}/*.py*
%{python3_sitelib}/%{pypi_name}/py.typed
%{python3_sitelib}/%{pypi_name}/__pycache__/*.pyc

%changelog
* Fri Sep 11 2026 Devrim Gunduz <devrim@gunduz.org> - 26.1.0-2PGDG
- Migrate %%python3_sitelib off the removed distutils.sysconfig module
  to sysconfig.get_path()
- Switch to pyproject builds
- Remove Fedora <= 42 support
- Add missing Fedora 44 pin (python3.14)

* Mon Aug 31 2026 Devrim Gunduz <devrim@gunduz.org> - 26.1.0-1PGDG
- Update to 26.1.0 per changes described at:
  https://github.com/python-attrs/attrs/releases/tag/26.1.0

* Tue Aug 25 2026 Devrim Gunduz <devrim@gunduz.org> - 22.1.0-44PGDG
- Build against the python3.13 alt-stack on Amazon Linux 2023, to keep
  the Python stack consistent across all packages in the repo.

* Tue Jun 2 2026 Devrim Gunduz <devrim@gunduz.org> - 22.1.0-43PGDG
- Update URL in attempt to fix
  https://github.com/pgdg-packaging/pgdg-rpms/issues/202

* Mon Oct 6 2025 Devrim Gunduz <devrim@gunduz.org> - 22.1.0-42PGDG
- Initial packaging for the PostgreSQL RPM repository to satisfy
  pg_activity dependency. Package is for RHEL 8 only.
