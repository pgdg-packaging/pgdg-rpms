%global modname prettytable

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
%if 0%{?suse_version} >= 1500
%global	__ospython %{_bindir}/python3.11
%global	python3_pkgversion 311
%endif

%{expand: %%global pybasever %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:4])"`)}
%global python3_sitelib %(%{__ospython} -Esc "import sysconfig; print(sysconfig.get_path('purelib', vars={'platbase': '/usr', 'base': '%{_prefix}'}))")

Name:		python%{python3_pkgversion}-%{modname}
Version:	3.4.0
Release:	47PGDG%{dist}.1
Summary:	Python library to display tabular data in tables

License:	BSD-3-Clause
URL:		https://github.com/jazzband/%{modname}
Source0:	https://files.pythonhosted.org/packages/source/p/prettytable/prettytable-3.4.0.tar.gz

BuildArch:	noarch

BuildRequires:	python%{python3_pkgversion}-devel
BuildRequires:	python%{python3_pkgversion}-setuptools
BuildRequires:	sed

Provides:	python%{python3_pkgversion}dist(prettytable)

%description
PrettyTable is a simple Python library designed to make it quick and easy to
represent tabular data in visually appealing ASCII tables. It was inspired by
the ASCII tables used in the PostgreSQL shell psql. PrettyTable allows for
selection of which columns are to be printed, independent alignment of columns
(left or right justified or centred) and printing of "sub-tables" by specifying
a row range.

%prep
%autosetup -n %{modname}-%{version}
sed -i -e '/^*!\//, 1d' src/prettytable/*.py

%build
%{__ospython} setup.py build

%install
%{__ospython} setup.py install --no-compile --root %{buildroot}
%if 0%{?amzn} == 2023
# AL2023's brp-python-bytecompile doesn't auto-discover the python3.13
# alt-stack site-packages dir the way Fedora/RHEL's does, so __pycache__
# never gets populated. Bytecompile explicitly instead.
%py_byte_compile %{__ospython} %{buildroot}%{python3_sitelib}/%{modname}
%endif

%files
%doc README.md CHANGELOG.md
%license COPYING
%{python3_sitelib}/%{modname}-%{version}-py%{pybasever}.egg-info/
%{python3_sitelib}/%{modname}/*.py*
%{python3_sitelib}/%{modname}/__pycache__/*.py*

%changelog
* Fri Aug 28 2026 Devrim Gunduz <devrim@gunduz.org> - 3.4.0-47PGDG.1
- Package the .egg-info directory itself instead of globbing only its
  contents (egg-info/*), so RHEL/Fedora's pythondist.attr generator
  (which is anchored on the .egg-info directory entry) actually fires
  and emits the wcwidth runtime Requires. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/226

* Tue Aug 25 2026 Devrim Gunduz <devrim@gunduz.org> - 3.4.0-46PGDG.1
- Explicitly bytecompile with %%py_byte_compile on Amazon Linux 2023.
  AL2023's brp-python-bytecompile doesn't auto-discover the python3.13
  alt-stack site-packages dir, so __pycache__ was never populated and
  the build failed with a missing-file error.

* Tue Aug 25 2026 Devrim Gunduz <devrim@gunduz.org> - 3.4.0-45PGDG.1
- Build against the python3.13 alt-stack on Amazon Linux 2023, to keep
  the Python stack consistent across all packages in the repo.

* Mon Sep 22 2025 Devrim Gunduz <devrim@gunduz.org> - 3.4.0-44PGDG.1
- Add Fedora 43 support

* Tue May 20 2025 Devrim Gunduz <devrim@gunduz.org> - 3.4.0-44PGDG
- Define python3_sitelib macro globally. For some reason it does not
  build on RHEL 8 - aarch64 without this.

* Tue May 20 2025 Devrim Gunduz <devrim@gunduz.org> - 3.4.0-43PGDG
- Add Provides:

* Tue May 20 2025 Devrim Gunduz <devrim@gunduz.org> - 3.4.0-42PGDG
- Initial packaging for the PostgreSQL RPM repository to support Patroni
  on RHEL 9 and RHEL 8.
