%global python3_sitelib %(%{__python3} -Esc "import sysconfig; print(sysconfig.get_path('purelib', vars={'platbase': '/usr', 'base': '%{_prefix}'}))")

%global sname rohmu

Name:		python3-%{sname}
Version:	2.8.2
Release:	3PGDG%{?dist}
Epoch:		1
Summary:	Python library for building backup tools for databases

License:	Apache 2.0
URL:		https://github.com/aiven/%{sname}
Source0:	https://github.com/aiven/%{sname}/archive/refs/tags/releases/%{version}.tar.gz

BuildRequires:	python3-devel python3-pip python3-hatchling python3-hatch-vcs
BuildRequires:	pyproject-rpm-macros

Requires:	python3-azure-storage-blob
BuildArch:	noarch

%description
Rohmu is a Python library for building backup tools for databases providing
functionality for compression, encryption and transferring data between the
database and an object storage. Rohmu supports main public clouds such as
GCP, AWS and Azure for backup storage. Rohmu is used in various backup tools
such as PGHhoard for PostgreSQL, MyHoard for MySQL and Astacus for M3 and
ClickHouse and other databases.

%prep
%setup -q -n %{sname}-releases-%{version}
# This GitHub tag-archive source has no git metadata for hatch-vcs to
# derive a version from; switch [tool.hatch.version] to hatchling's
# built-in "env" source instead, read from PGDG_PACKAGE_VERSION below
sed -i 's/^source = "vcs"$/source = "env"\nvariable = "PGDG_PACKAGE_VERSION"/' pyproject.toml

%build
export PGDG_PACKAGE_VERSION=%{version}
%pyproject_wheel

%install
%pyproject_install

%files
%license LICENSE
%doc README.rst
%{python3_sitelib}/%{sname}-%{version}.dist-info/
%{python3_sitelib}/%{sname}/

%changelog
* Mon Sep 14 2026 Devrim Gündüz <devrim@gunduz.org> - 1:2.8.2-3PGDG
- Migrate %%python3_sitelib off the removed distutils.sysconfig module to
  sysconfig.get_path() (distutils is gone on Python 3.12+, e.g. Fedora's
  default python3.14)
- Switch to pyproject builds.

* Mon Aug 31 2026 Devrim Gündüz <devrim@gunduz.org> - 1:2.8.2-1PGDG
- Update to 2.8.2 per changes described at:
  https://github.com/aiven/rohmu/releases/tag/releases/2.8.2

* Tue Dec 17 2024 Devrim Gündüz <devrim@gunduz.org> - 1:1.0.9-2PGDG
- Add RHEL 10 support
- Add PGDG branding

* Mon Jan 23 2023 Devrim Gündüz <devrim@gunduz.org> - 1:1.0.9-1
- Initial packaging for PostgreSQL YUM repo, to satisfy pghoard dependency.
