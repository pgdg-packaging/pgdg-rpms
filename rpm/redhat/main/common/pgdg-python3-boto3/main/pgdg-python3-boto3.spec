%global modname boto3

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

Name:		python%{python3_pkgversion}-%{modname}
Version:	1.43.118
Release:	42PGDG%{?dist}
Summary:	The AWS SDK for Python

License:	Apache-2.0
URL:		https://github.com/boto/%{modname}
Source:		%{url}/archive/%{version}/%{modname}-%{version}.tar.gz
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

# Save space by hardlinking duplicate JSON resource files
BuildRequires:	hardlink

Requires:	python%{python3_pkgversion}-botocore
# The Python dependency generator of RHEL 8 does not run for python3.12,
# so add the runtime dependencies explicitly there.
%if 0%{?rhel} == 8
Requires:	python%{python3_pkgversion}-jmespath >= 0.7.1
Requires:	python%{python3_pkgversion}-s3transfer >= 0.19.0
%endif

%if 0%{?rhel} == 10
# Replace the EPEL package of the same module, which has the same files:
Obsoletes:	python3-boto3 < %{version}-%{release}
%endif

%description
Boto3 is the Amazon Web Services (AWS) Software Development Kit (SDK) for
Python, which allows Python developers to write software that makes use of
services like Amazon S3 and Amazon EC2.}

%prep
%setup -q -n %{modname}-%{version}

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
%py_byte_compile %{__ospython} %{buildroot}%{python3_sitelib}/%{modname}
%endif


# This saves, as of this writing, roughly 300kB in duplicate JSON resource
# files. Note that rpmlint will complain about cross-directory hardlinks, but
# that these are not a problem because the contents of a directory owned by
# this package are guaranteed to be on a single filesystem.
hardlink -c '%{buildroot}%{python3_sitelib}/%{modname}'

%files
%doc CHANGELOG.rst
%doc README.rst
%license LICENSE
%{python3_sitelib}/%{modname}-%{version}-py%{pybasever}.egg-info/
%{python3_sitelib}/%{modname}/*.py*
%{python3_sitelib}/%{modname}/__pycache__/*.py*
%{python3_sitelib}/%{modname}/data/*
%{python3_sitelib}/%{modname}/examples/*
%{python3_sitelib}/%{modname}/docs/*.py*
%{python3_sitelib}/%{modname}/docs/__pycache__/*
%{python3_sitelib}/%{modname}/dynamodb/*.py*
%{python3_sitelib}/%{modname}/dynamodb/__pycache__/*
%{python3_sitelib}/%{modname}/ec2/*.py*
%{python3_sitelib}/%{modname}/ec2/__pycache__/*
%{python3_sitelib}/%{modname}/resources/*.py*
%{python3_sitelib}/%{modname}/resources/__pycache__/*
%{python3_sitelib}/%{modname}/s3/*.py*
%{python3_sitelib}/%{modname}/s3/__pycache__/*

%changelog
* Sat Oct 24 2026 Devrim Gunduz <devrim@gunduz.org> - 1.43.118-42PGDG
- Add RHEL 10 support, without EPEL, and obsolete the EPEL python3-boto3
  package there. Start the release from 42, so that our packages win over
  EPEL's. Per https://github.com/pgdg-packaging/pgdg-rpms/issues/422
- SLES 16: Generate the runtime Requires from the Python metadata, and
  BuildRequire python-rpm-packaging for the Python dependency generators.
  The package did not require s3transfer and jmespath there, so it could not be
  imported. Per https://github.com/pgdg-packaging/pgdg-rpms/issues/427

* Fri Oct 23 2026 Devrim Gunduz <devrim@gunduz.org> - 1.43.118-1PGDG
- Update to 1.43.118 per changes described at:
  https://pypi.org/project/boto3/1.43.118/
  Per https://github.com/pgdg-packaging/pgdg-rpms/issues/433

* Mon Oct 19 2026 Devrim Gunduz <devrim@gunduz.org> - 1.43.115-1PGDG
- Update to 1.43.115 per changes described at:
  https://pypi.org/project/boto3/1.43.115/
  Per https://github.com/pgdg-packaging/pgdg-rpms/issues/405
- Add explicit runtime dependencies on RHEL 8, where the Python
  dependency generator does not run for python3.12.

* Wed Oct 14 2026 Devrim Gunduz <devrim@gunduz.org> - 1.43.114-1PGDG
- Update to 1.43.114 per changes described at:
  https://pypi.org/project/boto3/1.43.114/
  Per https://github.com/pgdg-packaging/pgdg-rpms/issues/382

* Wed Oct 14 2026 Devrim Gunduz <devrim@gunduz.org> - 1.43.113-1PGDG
- Update to 1.43.113 per changes described at:
  https://pypi.org/project/boto3/1.43.113/
  Per https://github.com/pgdg-packaging/pgdg-rpms/issues/374

* Mon Oct 12 2026 Devrim Gunduz <devrim@gunduz.org> - 1.43.112-1PGDG
- Update to 1.43.112 per changes described at:
  https://pypi.org/project/boto3/1.43.112/
  Per https://github.com/pgdg-packaging/pgdg-rpms/issues/365

* Fri Oct 9 2026 Devrim Gunduz <devrim@gunduz.org> - 1.43.111-1PGDG
- Update to 1.43.111 per changes described at:
  https://pypi.org/project/boto3/1.43.111/
- Bytecompile on SLES, too. The SLES 16 build never worked, because
  no __pycache__ files were created there.

* Fri Sep 11 2026 Devrim Gunduz <devrim@gunduz.org> - 1.43.83-2PGDG
- Remove Fedora <= 42 support
- Fix Fedora 44 mapped to python3.15 instead of python3.14
- Add missing BR (python3-setuptools)

* Mon Aug 31 2026 Devrim Gunduz <devrim@gunduz.org> - 1.43.83-1PGDG
- Update to 1.43.83 per changes described at:
  https://pypi.org/project/boto3/1.43.83/

* Fri Aug 28 2026 Devrim Gunduz <devrim@gunduz.org> - 1.38.19-6PGDG
- Package the .egg-info directory itself instead of globbing only its
  contents (egg-info/*), so RHEL/Fedora's pythondist.attr generator
  (which is anchored on the .egg-info directory entry) actually fires
  and emits the correct runtime Requires. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/226

* Tue Aug 25 2026 Devrim Gunduz <devrim@gunduz.org> - 1.38.19-5PGDG
- Explicitly bytecompile with %%py_byte_compile on Amazon Linux 2023.
  AL2023's brp-python-bytecompile doesn't auto-discover the python3.13
  alt-stack site-packages dir, so __pycache__ was never populated and
  the build failed with a missing-file error.

* Tue Aug 25 2026 Devrim Gunduz <devrim@gunduz.org> - 1.38.19-4PGDG
- Build against the python3.13 alt-stack on Amazon Linux 2023, to keep
  the Python stack consistent across all packages in the repo.

* Mon Feb 23 2026 Devrim Gunduz <devrim@gunduz.org> - 1.38.19-3PGDG
- Add Fedora 44 and SLES 16 support. Need it for an internal sync script
  on SLES 16.

* Mon Sep 22 2025 Devrim Gunduz <devrim@gunduz.org> - 1.38.19-2PGDG.1
- Add Fedora 43 support

* Sat May 31 2025 Devrim Gunduz <devrim@gunduz.org> - 1.38.19-2PGDG
- Add missing botocore dependency, per:
  https://github.com/pgdg-packaging/pgdg-rpms/issues/36

* Tue May 20 2025 Devrim Gunduz <devrim@gunduz.org> - 1.38.19-1PGDG
- Initial packaging for the PostgreSQL RPM repository to support Patroni
  on RHEL 9 and 8.
