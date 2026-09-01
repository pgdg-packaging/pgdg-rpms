
%if 0%{?fedora} >= 40 || 0%{?rhel} >= 10
%{expand: %%global py3ver %(echo `%{__python3} -c "import sys; sys.stdout.write(sys.version[:4])"`)}
%else
%{expand: %%global py3ver %(echo `%{__python3} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%endif

%global python3_sitelib %(%{__python3} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")

%global sname rohmu

Name:		python3-%{sname}
Version:	2.8.2
Release:	1PGDG%{?dist}
Epoch:		1
Summary:	Python library for building backup tools for databases

License:	Apache 2.0
URL:		https://github.com/aiven/%{sname}
Source0:	https://github.com/aiven/%{sname}/archive/refs/tags/releases/%{version}.tar.gz

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

%build
CFLAGS="%{optflags}" %{__python3} setup.py build

%install
%{__python3} setup.py install --skip-build --root %{buildroot}

%files
%doc README.rst
%{python3_sitelib}/%{sname}-%{version}-py%{py3ver}.egg-info
%dir %{python3_sitelib}/%{sname}
%{python3_sitelib}/%{sname}/*

%changelog
* Mon Aug 31 2026 Devrim Gündüz <devrim@gunduz.org> - 1:2.8.2-1PGDG
- Update to 2.8.2 per changes described at:
  https://github.com/aiven/rohmu/releases/tag/releases/2.8.2

* Tue Dec 17 2024 Devrim Gündüz <devrim@gunduz.org> - 1:1.0.9-2PGDG
- Add RHEL 10 support
- Add PGDG branding

* Mon Jan 23 2023 Devrim Gündüz <devrim@gunduz.org> - 1:1.0.9-1
- Initial packaging for PostgreSQL YUM repo, to satisfy pghoard dependency.
