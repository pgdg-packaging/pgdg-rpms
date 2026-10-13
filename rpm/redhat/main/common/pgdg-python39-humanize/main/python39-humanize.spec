%global pypi_name humanize

%global __ospython %{_bindir}/python3.9
%if 0%{?fedora} >= 35
%{expand: %%global pyver %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:4])"`)}
%else
%{expand: %%global pyver %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%endif
%global python39_sitelib %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")

Name:		python39-humanize
Version:	3.13.1
Release:	42%{?dist}
Summary:	Turns dates in to human readable format, e.g '3 minutes ago'

License:	MIT
URL:		https://github.com/jmoiron/humanize
Source0:	%{pypi_source humanize}

BuildArch:	noarch
BuildRequires:	python39-devel
Requires:	python39

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

%files -n python39-humanize
%doc README.md
%{python39_sitelib}/%{pypi_name}/*.py
%{python39_sitelib}/%{pypi_name}/locale/*
%{python39_sitelib}/%{pypi_name}-0.0.0-py%{pyver}.egg-info
%{python39_sitelib}/%{pypi_name}/__pycache__/*.pyc

%changelog
* Sun Sep 18 2022 Devrim Gunduz <devrim@gunduz.org> 3.13.1-42
- Initial packaging for the PostgreSQL RPM repository to satisfy
  pg_activity dependency. Package is RHEL 8 only.
