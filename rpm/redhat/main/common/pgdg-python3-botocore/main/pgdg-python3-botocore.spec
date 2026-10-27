%global pypi_name botocore

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

%{expand: %%global pybasever %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:4])"`)}
%global python3_sitelib %(%{__ospython} -Esc "import sysconfig; print(sysconfig.get_path('purelib', vars={'platbase': '/usr', 'base': '%{_prefix}'}))")

%if 0%{?suse_version}
# SUSE only generates runtime Requires from the Python metadata when asked
# to; Fedora and RHEL do it by default.
%{?python_enable_dependency_generator}
%endif

Name:		python%{python3_pkgversion}-%{pypi_name}
# NOTICE - Updating this package requires updating python-boto3
Version:	1.43.119
Release:	42PGDG%{?dist}
Summary:	Low-level, data-driven core of boto 3

License:	Apache-2.0
URL:		https://github.com/boto/botocore
Source0:	https://files.pythonhosted.org/packages/source/b/botocore/botocore-%{version}.tar.gz

BuildArch:	noarch
BuildRequires:	python%{python3_pkgversion}-devel
BuildRequires:	python%{python3_pkgversion}-setuptools
%if 0%{?suse_version} >= 1500
BuildRequires:	python-rpm-macros
%endif
%if 0%{?suse_version} >= 1600
# SUSE's Python dependency generators. python3-devel pulls this in, but
# python%%{python3_pkgversion}-devel does not.
BuildRequires:	python-rpm-packaging
%endif
# The Python dependency generator of RHEL 8 does not run for python3.12,
# so add the runtime dependencies explicitly there.
%if 0%{?rhel} == 8
Requires:	python%{python3_pkgversion}-dateutil >= 2.1
Requires:	python%{python3_pkgversion}-jmespath >= 0.7.1
Requires:	python%{python3_pkgversion}-urllib3 >= 1.25.4
%endif

Provides:	bundled(python%{python3_version}-six) = 1.16.0
Provides:	bundled(python%{python3_version}-requests) = 2.7.0

%if 0%{?rhel} == 10
# Replace the EPEL package of the same module, which has the same files:
Obsoletes:	python3-botocore < %{version}-%{release}
%endif

%description
A low-level interface to a growing number of Amazon Web Services. The
botocore package is the foundation for the AWS CLI as well as boto3.}

%prep
%autosetup -n %{pypi_name}-%{version} -p1
# Remove online tests
rm -vr tests/integration
# This test tried to import tests/cmd-runner which failed as the code was
# unable to import "botocore". I'm not 100% sure why this happened but for now
# just exclude this one test and run all the other functional tests.
rm -vr tests/functional/leak
# Allow dateutil 3.x. botocore only uses dateutil.parser, tzutc and tzlocal,
# which did not change in 3.0.0:
sed -i 's/python-dateutil>=2.1,<3.0.0/python-dateutil>=2.1/' setup.py setup.cfg
grep -q "'python-dateutil>=2.1'," setup.py

%build
%{__ospython} setup.py build

%install
%{__ospython} setup.py install --no-compile --root %{buildroot}
# Create __pycache__ directories and their contents in SLES *too*:
%if 0%{?suse_version}
%{expand:%%python%{python3_pkgversion}_compile}
%endif
%if 0%{?amzn} == 2023
# AL2023's brp-python-bytecompile doesn't auto-discover the python3.13
# alt-stack site-packages dir the way Fedora/RHEL's does, so __pycache__
# never gets populated. Bytecompile explicitly instead.
%py_byte_compile %{__ospython} %{buildroot}%{python3_sitelib}/%{pypi_name}
%endif

%files
%doc README.rst
%license LICENSE.txt
%{python3_sitelib}/%{pypi_name}-%{version}-py%{pybasever}.egg-info/
%{python3_sitelib}/%{pypi_name}/*

%changelog
* Tue Oct 27 2026 Devrim Gunduz <devrim@gunduz.org> - 1.43.119-42PGDG
- Update to 1.43.119 per changes described at:
  https://pypi.org/project/botocore/1.43.119/

* Sun Oct 25 2026 Devrim Gunduz <devrim@gunduz.org> - 1.43.118-42PGDG
- Add RHEL 10 support, without EPEL, and obsolete the EPEL python3-botocore
  package there. Start the release from 42, so that our packages win over
  EPEL's. Per https://github.com/pgdg-packaging/pgdg-rpms/issues/422
- SLES 16: Generate the runtime Requires from the Python metadata, and
  BuildRequire python-rpm-packaging for the Python dependency generators.
  The package did not require jmespath, dateutil and urllib3 there, so
  botocore could not be imported. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/427

* Sat Oct 24 2026 Devrim Gunduz <devrim@gunduz.org> - 1.43.118-2PGDG
- Allow dateutil 3.x: the generated "python-dateutil < 3" Requires
  would make python3.12-dateutil 3.0.0 conflict with botocore on RHEL 9.
  Per https://github.com/pgdg-packaging/pgdg-rpms/issues/427

* Fri Oct 23 2026 Devrim Gunduz <devrim@gunduz.org> - 1.43.118-1PGDG
- Update to 1.43.118 per changes described at:
  https://pypi.org/project/botocore/1.43.118/
  Per https://github.com/pgdg-packaging/pgdg-rpms/issues/432

* Mon Oct 19 2026 Devrim Gunduz <devrim@gunduz.org> - 1.43.115-1PGDG
- Update to 1.43.115 per changes described at:
  https://pypi.org/project/botocore/1.43.115/
  Per https://github.com/pgdg-packaging/pgdg-rpms/issues/406
- Add explicit runtime dependencies on RHEL 8, where the Python
  dependency generator does not run for python3.12.

* Wed Oct 14 2026 Devrim Gunduz <devrim@gunduz.org> - 1.43.114-1PGDG
- Update to 1.43.114 per changes described at:
  https://pypi.org/project/botocore/1.43.114/
  Per https://github.com/pgdg-packaging/pgdg-rpms/issues/383

* Wed Oct 14 2026 Devrim Gunduz <devrim@gunduz.org> - 1.43.113-1PGDG
- Update to 1.43.113 per changes described at:
  https://pypi.org/project/botocore/1.43.113/
  Per https://github.com/pgdg-packaging/pgdg-rpms/issues/375

* Mon Oct 12 2026 Devrim Gunduz <devrim@gunduz.org> - 1.43.112-1PGDG
- Update to 1.43.112 per changes described at:
  https://pypi.org/project/botocore/1.43.112/
  Per https://github.com/pgdg-packaging/pgdg-rpms/issues/366

* Fri Oct 9 2026 Devrim Gunduz <devrim@gunduz.org> - 1.43.111-1PGDG
- Update to 1.43.111 per changes described at:
  https://pypi.org/project/botocore/1.43.111/
- Bytecompile on SLES, too, so that the package ships the
  __pycache__ files like on the other distros.

* Fri Sep 11 2026 Devrim Gunduz <devrim@gunduz.org> - 1.43.83-2PGDG
- Remove Fedora <= 42 support
- Fix Fedora 44 mapped to python3.15 instead of python3.14
- Add missing BR (python3-setuptools)

* Mon Aug 31 2026 Devrim Gunduz <devrim@gunduz.org> - 1.43.83-1PGDG
- Update to 1.43.83 per changes described at:
  https://pypi.org/project/botocore/1.43.83/

* Fri Aug 28 2026 Devrim Gunduz <devrim@gunduz.org> - 1.38.19-5PGDG
- Package the .egg-info directory itself instead of globbing only its
  contents (egg-info/*), so RHEL/Fedora's pythondist.attr generator
  (which is anchored on the .egg-info directory entry) actually fires
  and emits the correct runtime Requires. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/226

* Tue Aug 25 2026 Devrim Gunduz <devrim@gunduz.org> - 1.38.19-4PGDG
- Add a local python3_sitelib override tied to __ospython (this spec
  was the only one in the pgdg-python3-* family missing it), and
  explicitly bytecompile with %%py_byte_compile on Amazon Linux 2023.
  Without the override, %%files would look for installed files under
  the system default python3's site-packages instead of the
  python3.13 alt-stack's, since AL2023's default python3 isn't 3.13
  (unlike Fedora/RHEL/SUSE, where the chosen alt version always
  happens to match the distro's actual default). AL2023's
  brp-python-bytecompile also doesn't auto-discover the alt-stack
  site-packages dir, so __pycache__ was never populated either.

* Tue Aug 25 2026 Devrim Gunduz <devrim@gunduz.org> - 1.38.19-3PGDG
- Build against the python3.13 alt-stack on Amazon Linux 2023, to keep
  the Python stack consistent across all packages in the repo.

* Mon Feb 23 2026 Devrim Gunduz <devrim@gunduz.org> - 1.38.19-3PGDG
- Add Fedora 44 and SLES 16 support. Need it for an internal sync script
  on SLES 16.

* Mon Sep 22 2025 Devrim Gunduz <devrim@gunduz.org> - 1.38.19-1PGDG.1
- Add Fedora 43 support

* Sat May 31 2025 Devrim Gunduz <devrim@gunduz.org> - 1.38.19-1PGDG
- Inıtial packaging for the PostgreSQL RPM repository to support Patroni
  on RHEL 9 and RHEL 8.
