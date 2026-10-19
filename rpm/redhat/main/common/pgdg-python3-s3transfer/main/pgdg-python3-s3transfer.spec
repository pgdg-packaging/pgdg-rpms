# Built for the python3.12 stack of RHEL 8 and 9 only, where the
# OS package is built for the default Python. boto3 needs it.
%if 0%{?rhel} && 0%{?rhel} <= 9
%global	__ospython %{_bindir}/python3.12
%global	python3_pkgversion 3.12
%endif

%{expand: %%global pybasever %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:4])"`)}
%global python3_sitelib %(%{__ospython} -Esc "import sysconfig; print(sysconfig.get_path('purelib', vars={'platbase': '/usr', 'base': '%{_prefix}'}))")

%global	modname s3transfer

Name:		python%{python3_pkgversion}-%{modname}
Version:	0.19.3
Release:	1PGDG%{?dist}
Summary:	An Amazon S3 Transfer Manager

License:	Apache-2.0
URL:		https://github.com/boto/%{modname}
Source0:	https://files.pythonhosted.org/packages/source/s/%{modname}/%{modname}-%{version}.tar.gz
BuildArch:	noarch

BuildRequires:	python%{python3_pkgversion}-devel
BuildRequires:	python%{python3_pkgversion}-setuptools

Requires:	python%{python3_pkgversion}-botocore

%description
S3transfer is a Python library for managing Amazon S3 transfers.

%prep
%setup -q -n %{modname}-%{version}

%build
%{__ospython} setup.py build

%install
%{__ospython} setup.py install --no-compile --root %{buildroot}

%files
%doc README.rst
%license LICENSE.txt NOTICE.txt
%{python3_sitelib}/%{modname}-%{version}-py%{pybasever}.egg-info/
%{python3_sitelib}/%{modname}/

%changelog
* Tue Oct 20 2026 Devrim Gunduz <devrim@gunduz.org> - 0.19.3-1PGDG
- Initial packaging for the PostgreSQL RPM repository, for boto3
  on RHEL 9 and 8.
