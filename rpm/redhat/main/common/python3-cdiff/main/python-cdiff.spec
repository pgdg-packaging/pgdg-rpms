%if 0%{?fedora} && 0%{?fedora} == 44
%global python3_pkgversion 3.14
%endif
%if 0%{?fedora} && 0%{?fedora} == 43
%global python3_pkgversion 3.14
%endif
%if 0%{?rhel} && 0%{?rhel} <= 10
%global	python3_pkgversion 3.12
%endif
%if 0%{?amzn} == 2023
%global	__python3 %{_bindir}/python3.13
%global	python3_pkgversion 3.13
%endif
%if 0%{?suse_version} == 1500
%global	python3_pkgversion 311
# Build the python311 flavor with the SUSE pyproject macros, instead of
# the default python3 (3.6):
%global	pythons python311
%global	python3_sitelib %{_prefix}/lib/python3.11/site-packages
%endif
%if 0%{?suse_version} == 1600
%global	python3_pkgversion 313
%endif
%global sname cdiff

Name:		python3-%{sname}
Version:	1.0
Release:	48PGDG%{?dist}
Summary:	View colored, incremental diff in a workspace or from stdin, with side by side and auto pager support

License:	BSD
URL:		https://pypi.org/project/%{sname}/
Source0:	https://files.pythonhosted.org/packages/69/6c/301876940e760a8b46c1caacf08c298f511f517c70eec32e43f38e9cc6f5/%{sname}-%{version}.tar.gz

BuildArch:	noarch

Requires:	less python3
BuildRequires:	python%{python3_pkgversion}-devel
BuildRequires:	python%{python3_pkgversion}-pip
BuildRequires:	python%{python3_pkgversion}-setuptools
BuildRequires:	python%{python3_pkgversion}-wheel

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
* Sun Oct 11 2026 Devrim Gunduz <devrim@gunduz.org> - 1.0-48PGDG
- Build the python311 flavor on SLES 15. The SUSE pyproject macros built
  for the default python3 (3.6), so the build failed there. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/226
- Set python3_sitelib to the python3.11 one on SLES 15, too: the SUSE macro
  points to the default python3 (3.6).

* Fri Sep 11 2026 Devrim Gunduz <devrim@gunduz.org> - 1.0-47PGDG
- Remove Fedora <= 42 support
- Add missing Fedora 44 pin (python3.14)

* Thu Sep 10 2026 Devrim Gunduz <devrim@gunduz.org> - 1.0-46PGDG
- Add missing BR

* Tue Aug 25 2026 Devrim Gunduz <devrim@gunduz.org> - 1.0-45PGDG
- Also set __python3 (not just __ospython) for Amazon Linux 2023, so
  %pyproject_wheel/%pyproject_install actually build against python3.13
  instead of silently falling back to the system default python3
  (__ospython only affects this repo's own macro computations, not
  RPM's own pyproject/site-packages macros).

* Tue Aug 25 2026 Devrim Gündüz <devrim@gunduz.org> - 1.0-44PGDG
- Build against the python3.13 alt-stack on Amazon Linux 2023, to keep
  the Python stack consistent across all packages in the repo.

* Thu May 7 2026 Devrim Gündüz <devrim@gunduz.org> - 1.0-43PGDG
- Add missing BRs

* Sat Oct 25 2025 Devrim Gündüz <devrim@gunduz.org> - 1.0-42PGDG
- Switch to pyproject build

* Wed Aug 5 2020 Devrim Gündüz <devrim@gunduz.org> - 1.0-1
- Initial packaging for PostgreSQL RPM repository, to satisfy patroni dependency.
