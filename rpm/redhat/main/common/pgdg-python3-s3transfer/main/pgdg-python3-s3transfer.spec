%pgdg_python3_setup

# Built for the python3.12 stack of RHEL 8 and 9, where the OS package is
# built for the default Python, and for RHEL 10, which has none. boto3
# needs it.

%{expand: %%global pybasever %(echo `%{__python3} -c "import sys; sys.stdout.write(sys.version[:4])"`)}
%global python3_sitelib %(%{__python3} -Esc "import sysconfig; print(sysconfig.get_path('purelib', vars={'platbase': '/usr', 'base': '%{_prefix}'}))")

%global	modname s3transfer

Name:		python%{python3_pkgversion}-%{modname}
Version:	0.19.3
Release:	43PGDG%{?dist}
Summary:	An Amazon S3 Transfer Manager

License:	Apache-2.0
URL:		https://github.com/boto/%{modname}
Source0:	https://files.pythonhosted.org/packages/source/s/%{modname}/%{modname}-%{version}.tar.gz
BuildArch:	noarch

BuildRequires:	python%{python3_pkgversion}-devel
BuildRequires:	python%{python3_pkgversion}-setuptools

Requires:	python%{python3_pkgversion}-botocore

%if 0%{?rhel} == 10
# Replace the EPEL package of the same module, which has the same files:
Obsoletes:	python3-s3transfer < %{version}-%{release}
%endif

%description
S3transfer is a Python library for managing Amazon S3 transfers.

%prep
%setup -q -n %{modname}-%{version}

%build
%{__python3} setup.py build

%install
%{__python3} setup.py install --no-compile --root %{buildroot}

%files
%doc README.rst
%license LICENSE.txt NOTICE.txt
%{python3_sitelib}/%{modname}-%{version}-py%{pybasever}.egg-info/
%{python3_sitelib}/%{modname}/

%changelog
* Wed Oct 28 2026 Devrim Gunduz <devrim@gunduz.org> - 0.19.3-43PGDG
- Use %%pgdg_python3_setup from pgdg-srpm-macros 2.5.0 instead of the
  per-distro Python block and the __ospython macro. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/462

* Sat Oct 24 2026 Devrim Gunduz <devrim@gunduz.org> - 0.19.3-42PGDG
- Add RHEL 10 support, for boto3 without EPEL.
- RHEL 10: Obsolete the EPEL python3-s3transfer package. Start the release
  from 42, so that our packages win over EPEL's. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/422

* Tue Oct 20 2026 Devrim Gunduz <devrim@gunduz.org> - 0.19.3-1PGDG
- Initial packaging for the PostgreSQL RPM repository, for boto3
  on RHEL 9 and 8.
