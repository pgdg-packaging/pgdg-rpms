%global pythons python311
%global sname humanize
%global __ospython %{_bindir}/python3.11

%{expand: %%global py3ver %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:4])"`)}
%global python311_sitelib %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")

Name:		python311-%{sname}
Version:	3.13.1
Release:	43PGDG%{?dist}
Summary:	Turns dates in to human readable format, e.g '3 minutes ago'

License:	MIT
URL:		https://github.com/jmoiron/%{sname}
Source0:	https://pypi.python.org/packages/source/h/%{sname}/%{sname}-%{version}.tar.gz

BuildArch:	noarch
BuildRequires:	python311-devel python311-hatchling

%description
This modest package contains various common humanization utilities, like turning\
a number into a fuzzy human readable duration ('3 minutes ago') or into a human\
readable size or throughput.\

%package -n python3-%{sname}
Summary:	%summary

%description -n python3-%{sname}
This modest package contains various common humanization utilities, like turning
a number into a fuzzy human readable duration ('3 minutes ago') or into a human
readable size or throughput.

%prep
%setup -q -n %{sname}-%{version}

# Remove shebangs from libs.
for lib in src/%{sname}/time.py src/%{sname}/filesize.py src/%{sname}/number.py; do
 sed '1{\@^#!/usr/bin/env python@d}' $lib > $lib.new &&
 touch -r $lib $lib.new && mv $lib.new $lib
done

# Remove .po files
find -name '*.po' -delete

%build
%{__ospython} setup.py build

%install
%{__ospython} setup.py install --no-compile --root %{buildroot}

%files
%doc README.md
%{python311_sitelib}/humanize-0.0.0-py%{py3ver}.egg-info/
%{python311_sitelib}/humanize/*

%changelog
* Fri Aug 28 2026 Devrim Gündüz <devrim@gunduz.org> - 3.13.1-43PGDG
- Package the .egg-info directory itself instead of globbing only its
  contents (egg-info/*), so RHEL/Fedora's pythondist.attr generator
  (which is anchored on the .egg-info directory entry) actually fires
  and emits the correct runtime Requires. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/226

* Mon Feb 19 2024 Devrim Gündüz <devrim@gunduz.org> - 3.13.1-42PGDG
- Initial packaging for the PostgreSQL RPM repository to support
  pg_activity dependency on SLES 15.
