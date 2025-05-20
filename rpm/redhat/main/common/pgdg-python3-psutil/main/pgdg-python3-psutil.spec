%global modname psutil

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
Version:	6.1.1
Release:	43PGDG%{?dist}
Summary:	A process and system utilities module for Python

License:	BSD-3-Clause
URL:		https://github.com/giampaolo/%{modname}
Source:		%{url}/archive/release-%{version}/%{modname}-%{version}.tar.gz

BuildRequires:	gcc sed python%{python3_pkgversion}-devel

Provides:	python%{python3_pkgversion}dist(psutil)

%description
psutil is a module providing an interface for retrieving information on all
running processes and system utilization (CPU, memory, disks, network, users) in
a portable way by using Python, implementing many functionalities offered by
command line tools such as: ps, top, df, kill, free, lsof, free, netstat,
ifconfig, nice, ionice, iostat, iotop, uptime, pidof, tty, who, taskset, pmap.

%prep
%autosetup -p1 -n %{modname}-release-%{version}

# Remove shebangs
find psutil -name \*.py | while read file; do
  sed -i.orig -e '1{/^#!/d}' $file && \
  touch -r $file.orig $file && \
  %{__rm} $file.orig
done

%build
%{__ospython} setup.py build

%install
%{__ospython} setup.py install --no-compile --root %{buildroot}

%files
%doc CREDITS HISTORY.rst README.rst
%exclude %{python3_sitearch}/%{modname}/tests
%{python3_sitearch}/%{modname}-%{version}-py%{pybasever}.egg-info/*
%{python3_sitearch}/%{modname}/*.py*
%{python3_sitearch}/%{modname}/__pycache__/*.py*
%{python3_sitearch}/%{modname}/*.so

%changelog
* Tue May 20 2025 Devrim Gunduz <devrim@gunduz.org> - 6.1.1-43PGDG
- Define python3_sitelib macro globally. For some reason it does not
  build on RHEL 8 - aarch64 without this.

* Tue May 20 2025 Devrim Gunduz <devrim@gunduz.org> - 6.1.1-42PGDG
- Add Provides:

* Tue May 20 2025 Devrim Gunduz <devrim@gunduz.org> - 6.1.1-2PGDG
- Inıtial packaging for the PostgreSQL RPM repository to support Patroni
  on RHEL 9 and RHEL 8.
