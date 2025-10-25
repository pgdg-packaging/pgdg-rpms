%if 0%{?fedora} && 0%{?fedora} == 43
%global python3_pkgversion 3.14
%endif
%if 0%{?fedora} && 0%{?fedora} <= 42
%global	python3_pkgversion 3.13
%endif
%if 0%{?rhel} && 0%{?rhel} <= 10
%global	python3_pkgversion 3.12
%endif
%if 0%{?suse_version} == 1500
%global	python3_pkgversion 311
%endif
%if 0%{?suse_version} == 1600
%global	python3_pkgversion 313
%endif
%global sname cdiff

Name:		python3-%{sname}
Version:	1.0
Release:	2PGDG%{?dist}
Summary:	View colored, incremental diff in a workspace or from stdin, with side by side and auto pager support

License:	BSD
URL:		https://pypi.org/project/%{sname}/
Source0:	https://files.pythonhosted.org/packages/69/6c/301876940e760a8b46c1caacf08c298f511f517c70eec32e43f38e9cc6f5/%{sname}-%{version}.tar.gz

BuildArch:	noarch

Requires:	less python3
BuildRequires:	python%{python3_pkgversion}-devel
%if 0%{?suse_version} >= 1500
BuildRequires:	python-rpm-macros
%else
BuildRequires:	pyproject-rpm-macros
%endif

Provides:	python3-%{sname}%{?_isa} = %{version}-%{release}
Provides:	python%{python3_pkgversion}dist(%{name}) = %{version}-%{release}

%description
Term based tool to view colored, incremental diff in a
Git/Mercurial/Svn workspace or from stdin, with side by side
and auto pager support. Requires python (>= 2.5.0) and less.

%prep
%setup -q -n %{sname}-%{version}

%build
%pyproject_wheel

%install
%pyproject_install

%files
%license LICENSE
%doc README.rst CHANGES.rst
%{_bindir}/cdiff
%{python3_sitelib}/__pycache__/cdiff*
%{python3_sitelib}/cdiff*

%changelog
* Sat Oct 25 2025 Devrim Gündüz <devrim@gunduz.org> - 1.0-42PGDG
- Switch to pyproject build

* Wed Aug 5 2020 Devrim Gündüz <devrim@gunduz.org> - 1.0-1
- Initial packaging for PostgreSQL RPM repository, to satisfy patroni dependency.
