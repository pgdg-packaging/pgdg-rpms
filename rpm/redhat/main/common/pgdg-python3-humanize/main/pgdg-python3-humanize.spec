%global pypi_name humanize
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
%if 0%{?suse_version} == 1500
%global	__ospython %{_bindir}/python3.11
%global	python3_pkgversion 311
%endif
%if 0%{?suse_version} == 1600
%global	__ospython %{_bindir}/python3.13
%global	python3_pkgversion 313
%endif

%{expand: %%global pyver %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:4])"`)}

%global python_sitelib %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")

Name:		python%{python3_pkgversion}-humanize
Version:	3.13.1
Release:	42PGDG%{?dist}
Summary:	Turns dates in to human readable format, e.g '3 minutes ago'

License:	MIT
URL:		https://github.com/jmoiron/humanize
Source0:	%{pypi_source humanize}

BuildArch:	noarch
BuildRequires:	python%{python3_pkgversion}-devel
Requires:	python%{python3_pkgversion}

%global _description\
This modest package contains various common humanization utilities, like turning\
a number into a fuzzy human readable duration ('3 minutes ago') or into a human\
readable size or throughput.\

%description %_description

%prep
%autosetup -n humanize-%{version}

# Remove shebangs from libs.
for lib in src/humanize/time.py src/humanize/filesize.py src/humanize/number.py; do
 sed '1{\@^#!/usr/bin/env python@d}' $lib > $lib.new &&
 touch -r $lib $lib.new && mv $lib.new $lib
done

# Remove .po files
find -name '*.po' -delete

# Don't run coverage report during %%check
sed -i '/pytest-cov/d' setup.cfg
sed -Ei 's/ ?--cov(-[^ ]+)? +[^ ]+//g' tox.ini

%build
%{__ospython} setup.py build

%install
%{__ospython} setup.py install -O1 --skip-build --root %{buildroot}

%files
%doc README.md
%{python3_sitelib}/%{pypi_name}/*.py
%{python3_sitelib}/%{pypi_name}/locale/*
%{python3_sitelib}/%{pypi_name}-0.0.0-py%{pyver}.egg-info
%{python3_sitelib}/%{pypi_name}/__pycache__/*.pyc

%changelog
* Mon Oct 6 2025 Devrim Gunduz <devrim@gunduz.org> - 3.13.1-42PGDG
- Initial packaging for the PostgreSQL RPM repository to satisfy
  pg_activity dependency. Package is RHEL 8 only.
