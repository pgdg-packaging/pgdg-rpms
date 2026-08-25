%global modname wcwidth

%if 0%{?fedora} && 0%{?fedora} == 43
%global __ospython %{_bindir}/python3.14
%global python3_pkgversion 3.14
%endif
%if 0%{?fedora} && 0%{?fedora} <= 42
%global	__ospython %{_bindir}/python3.13
%global	python3_pkgversion 3.13
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

%global python3_sitelib %(%{__ospython} -Esc "import sysconfig; print(sysconfig.get_path('purelib', vars={'platbase': '/usr', 'base': '%{_prefix}'}))")

Name:		python%{python3_pkgversion}-%{modname}
Version:	0.2.13
Release:	4PGDG%{dist}
Summary:	Measures number of Terminal column cells of wide-character codes

# part of the code is under HPND-Markus-Kuhn
License:	MIT AND HPND-Markus-Kuhn
URL:		https://github.com/jquast/%{modname}
Source:		https://files.pythonhosted.org/packages/source/w/%{modname}/%{modname}-%{version}.tar.gz
BuildArch:	noarch

Provides:	python%{python3_pkgversion}dist(wcwidth)

%if 0%{?suse_version} >= 1500
BuildRequires:	python-rpm-macros
%else
BuildRequires:	pyproject-rpm-macros
%endif

%description
This API is mainly for Terminal Emulator implementors, or those writing programs
that expect to interpreted by a terminal emulator and wish to determine the
printable width of a string on a Terminal.

%prep
%setup -q -n %{modname}-%{version}
# skip coverage checks
sed -i -e 's|--cov[^[:space:]]*||g' tox.ini

%build
%pyproject_wheel

%install
%pyproject_install

%files
%doc README.rst
%license LICENSE
%{python3_sitelib}/%{modname}-%{version}.dist-info/*
%{python3_sitelib}/%{modname}/*.py*
%{python3_sitelib}/%{modname}/__pycache__/*.py*

%changelog
* Tue Aug 25 2026 Devrim Gunduz <devrim@gunduz.org> - 0.2.13-4PGDG
- Build against the python3.13 alt-stack on Amazon Linux 2023, to keep
  the Python stack consistent across all packages in the repo.

* Mon Dec 29 2025 Devrim Gunduz <devrim@gunduz.org> - 0.2.13-3PGDG
- Add SLES support
- Switch to pyproject builds

* Tue Oct 7 2025 Devrim Gunduz <devrim@gunduz.org> - 0.2.13-2PGDG
- Provide dist(wcwidth). Needed at least on RHEL 9

* Mon Sep 22 2025 Devrim Gunduz <devrim@gunduz.org> - 0.2.13-1PGDG.1
- Add Fedora 43 support

* Tue May 20 2025 Devrim Gunduz <devrim@gunduz.org> - 0.2.3-1PGDG
- Initial packaging for the PostgreSQL RPM repository to support Patroni
  on RHEL 9 and RHEL 8.
