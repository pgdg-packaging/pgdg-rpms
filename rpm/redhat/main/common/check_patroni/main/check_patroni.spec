%if 0%{?fedora} && 0%{?fedora} == 44
%global __ospython %{_bindir}/python3.14
%global python3_pkgversion 3.14
%endif
%if 0%{?fedora} && 0%{?fedora} == 43
%global __ospython %{_bindir}/python3.14
%global python3_pkgversion 3.14
%endif
%if 0%{?rhel} && 0%{?rhel} <= 10
%global	__ospython %{_bindir}/python3.12
%global	python3_pkgversion 3.12
%endif
%if 0%{?amzn} == 2023
%global	__ospython %{_bindir}/python3.13
%global	__python3 %{_bindir}/python3.13
%global	python3_pkgversion 3.13
%endif
%if 0%{?suse_version} == 1500
%global	__ospython %{_bindir}/python3.11
%global	python3_pkgversion 311
# Build the python311 flavor with the SUSE pyproject macros, instead of
# the default python3 (3.6):
%global	pythons python311
%global	python3_sitelib %{_prefix}/lib/python3.11/site-packages
%endif
%if 0%{?suse_version} == 1600
%global	__ospython %{_bindir}/python3.13
%global	python3_pkgversion 313
%endif
%{expand: %%global py3ver %(echo `%{__python3} -c "import sys; sys.stdout.write(sys.version[:4])"`)}

%global sname check_patroni

%if 0%{?suse_version} >= 1600
# SUSE only generates runtime Requires from the Python metadata when asked
# to; Fedora and RHEL do it by default.
%{?python_enable_dependency_generator}
%endif

Name:		nagios-plugins-patroni
Version:	2.2.0
Release:	11PGDG%{dist}
Summary:	Patroni monitoring plugin for Nagios
License:	PostgreSQL
Url:		https://github.com/dalibo/%{sname}/
Source0:	https://github.com/dalibo/%{sname}/archive/refs/tags/v%{version}.tar.gz
BuildArch:	noarch
%if 0%{?suse_version} >= 1500
BuildRequires:	python-rpm-macros
BuildRequires:	python%{python3_pkgversion}-devel
BuildRequires:	python%{python3_pkgversion}-pip
BuildRequires:	python%{python3_pkgversion}-setuptools
BuildRequires:	python%{python3_pkgversion}-wheel
%if 0%{?suse_version} >= 1600
# SUSE's Python dependency generators. python3-devel pulls this in, but
# python%%{python3_pkgversion}-devel does not.
BuildRequires:	python-rpm-packaging
%endif
%else
BuildRequires:	pyproject-rpm-macros
# python%%{python3_pkgversion}-devel is what pulls python3-rpm-generators
# into the buildroot on RHEL/Fedora; pyproject-rpm-macros alone does not.
# Without it, neither python(abi) nor python%%{python3_pkgversion}dist(...)
# get generated. Per https://github.com/pgdg-packaging/pgdg-rpms/issues/228
BuildRequires:	python%{python3_pkgversion}-devel
BuildRequires:	python%{python3_pkgversion}-pip
BuildRequires:	python%{python3_pkgversion}-setuptools
BuildRequires:	python%{python3_pkgversion}-wheel
%endif
Requires:	nagios-plugins
%if 0%{?rhel} == 8
# The Python dependency generator of RHEL 8 does not run for python3.12,
# so add the runtime dependencies explicitly there.
Requires:	python%{python3_pkgversion}-attrs
Requires:	python%{python3_pkgversion}-click >= 7.1
Requires:	python%{python3_pkgversion}-nagiosplugin >= 1.3.2
Requires:	python%{python3_pkgversion}-requests
%endif
Provides:	%{sname} = %{version}

%description
check_patroni is a monitoring plugin of patroni for Nagios.

%prep
%setup -q -n %{sname}-%{version}

%build
%pyproject_wheel

%install
%pyproject_install

%files
%defattr(-,root,root,0755)
%doc docs
%license LICENSE
%{_bindir}/%{sname}
%{python3_sitelib}/%{sname}/*.py
%{python3_sitelib}/%{sname}-%{version}.dist-info/
%{python3_sitelib}/%{sname}/__pycache__/*.pyc

%changelog
* Mon Oct 26 2026 Devrim Gunduz <devrim@gunduz.org> - 2.2.0-11PGDG
- SLES 16: Generate the runtime Requires from the Python metadata, and
  BuildRequire python-rpm-packaging for the Python dependency generators.
  The package did not require attrs, click, nagiosplugin and requests there, so it could not be
  imported. Per https://github.com/pgdg-packaging/pgdg-rpms/issues/427
- RHEL 8: Require attrs, click, nagiosplugin and requests, which the
  Python dependency generator does not add there for python3.12.
- SUSE: BuildRequire python-devel, pip, setuptools and wheel, which the
  build needs, so that it builds in a clean build root, too.

* Fri Oct 23 2026 Devrim Gunduz <devrim@gunduz.org> - 2.2.0-10PGDG
- Add the missing python%%{python3_pkgversion}-wheel BR: setuptools on RHEL 8
  (68) cannot build wheels without it. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/422

* Sun Oct 11 2026 Devrim Gunduz <devrim@gunduz.org> - 2.2.0-9PGDG
- Build the python311 flavor on SLES 15. The SUSE pyproject macros built
  for the default python3 (3.6), so the build failed there. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/226
- Set python3_sitelib to the python3.11 one on SLES 15, too: the SUSE macro
  points to the default python3 (3.6).

* Fri Sep 11 2026 Devrim Gunduz <devrim@gunduz.org> - 2.2.0-8PGDG
- Remove Fedora <= 42 support
- Add missing Fedora 44 pin (python3.14)

* Thu Sep 10 2026 Devrim Gunduz <devrim@gunduz.org> - 2.2.0-7PGDG
- Add missing BR

* Fri Aug 28 2026 Devrim Gunduz <devrim@gunduz.org> - 2.2.0-6PGDG
- Add back python%{python3_pkgversion}-devel as a BuildRequires on the
  non-SLES branch, needed to pull python3-rpm-generators into the
  buildroot for this pyproject build. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/228

* Tue Aug 25 2026 Devrim Gunduz <devrim@gunduz.org> - 2.2.0-5PGDG
- Also set __python3 (not just __ospython) for Amazon Linux 2023, so
  %pyproject_wheel/%pyproject_install actually build against python3.13
  instead of silently falling back to the system default python3
  (__ospython only affects this repo's own macro computations, not
  RPM's own pyproject/site-packages macros).

* Tue Aug 25 2026 Devrim Gündüz <devrim@gunduz.org> 2.2.0-4PGDG
- Build against the python3.13 alt-stack on Amazon Linux 2023, to keep
  the Python stack consistent across all packages in the repo.

* Wed Oct 15 2025 Devrim Gündüz <devrim@gunduz.org> 2.2.0-3PGDG
- Fix builds on SLES

* Wed Oct 8 2025 Devrim Gündüz <devrim@gunduz.org> 2.2.0-2PGDG
- Add SLES 16 support
- Use Python 3.1x on all platforms
- Switch to pyproject build

* Sun Apr 13 2025 Devrim Gündüz <devrim@gunduz.org> 2.2.0-1PGDG
- Initial packaging for the PostgreSQL RPM repository
