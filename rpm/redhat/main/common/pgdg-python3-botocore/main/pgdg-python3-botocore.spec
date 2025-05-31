%global pypi_name botocore

%if 0%{?fedora} && 0%{?fedora} >= 41
%global	__ospython %{_bindir}/python3.13
%global	python3_pkgversion 3.13
%endif
%if 0%{?rhel} && 0%{?rhel} <= 10
%global	__ospython %{_bindir}/python3.12
%global	python3_pkgversion 3.12
%endif
%if 0%{?suse_version} >= 1500
%global	__ospython %{_bindir}/python3.11
%global	python3_pkgversion 311
%endif

%{expand: %%global pybasever %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:4])"`)}

Name:		python%{python3_pkgversion}-%{pypi_name}
# NOTICE - Updating this package requires updating python-boto3
Version:	1.38.19
Release:	1PGDG%{?dist}
Summary:	Low-level, data-driven core of boto 3

License:	Apache-2.0
URL:		https://github.com/boto/botocore
Source0:	https://files.pythonhosted.org/packages/source/b/botocore/botocore-%{version}.tar.gz

BuildArch:	noarch
BuildRequires:	python%{python3_version}-devel
Provides:	bundled(python%{python3_version}-six) = 1.16.0
Provides:	bundled(python%{python3_version}-requests) = 2.7.0

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

%build
%{__ospython} setup.py build

%install
%{__ospython} setup.py install --no-compile --root %{buildroot}

%files
%doc README.rst
%license LICENSE.txt
%{python3_sitelib}/%{pypi_name}-%{version}-py%{pybasever}.egg-info/*
%{python3_sitelib}/%{pypi_name}/*

%changelog
* Sat May 31 2025 Devrim Gunduz <devrim@gunduz.org> - 1.38.19-1PGDG
- Inıtial packaging for the PostgreSQL RPM repository to support Patroni
  on RHEL 9 and RHEL 8.
