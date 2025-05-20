%global modname boto3

%if 0%{?fedora} && 0%{?fedora} <= 42
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
%global python3_sitelib %(%{__ospython} -Esc "import sysconfig; print(sysconfig.get_path('purelib', vars={'platbase': '/usr', 'base': '%{_prefix}'}))")

Name:		python%{python3_pkgversion}-%{modname}
Version:	1.38.19
Release:	1PGDG%{?dist}
Summary:	The AWS SDK for Python

License:	Apache-2.0
URL:		https://github.com/boto/%{modname}
Source:		%{url}/archive/%{version}/%{modname}-%{version}.tar.gz
BuildArch:	noarch

BuildRequires:	python%{python3_pkgversion}-devel

# Save space by hardlinking duplicate JSON resource files
BuildRequires:	hardlink

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


# This saves, as of this writing, roughly 300kB in duplicate JSON resource
# files. Note that rpmlint will complain about cross-directory hardlinks, but
# that these are not a problem because the contents of a directory owned by
# this package are guaranteed to be on a single filesystem.
hardlink -c '%{buildroot}%{python3_sitelib}/%{modname}'

%files
%doc CHANGELOG.rst
%doc README.rst
%license LICENSE
%{python3_sitelib}/%{modname}-%{version}-py%{pybasever}.egg-info/*
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
* Tue May 20 2025 Devrim Gunduz <devrim@gunduz.org> - 1.38.19-1PGDG
- Initial packaging for the PostgreSQL RPM repository to support Patroni
  on RHEL 9 and 8.
