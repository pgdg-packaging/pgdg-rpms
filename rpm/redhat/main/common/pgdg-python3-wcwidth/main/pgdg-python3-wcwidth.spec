%global modname wcwidth

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
Version:	0.2.13
Release:	1PGDG%{dist}
Summary:	Measures number of Terminal column cells of wide-character codes

# part of the code is under HPND-Markus-Kuhn
License:	MIT AND HPND-Markus-Kuhn
URL:		https://github.com/jquast/%{modname}
Source:		https://files.pythonhosted.org/packages/source/w/%{modname}/%{modname}-%{version}.tar.gz
BuildArch:	noarch

%description
This API is mainly for Terminal Emulator implementors, or those writing programs
that expect to interpreted by a terminal emulator and wish to determine the
printable width of a string on a Terminal.

%prep
%setup -q -n %{modname}-%{version}
# skip coverage checks
sed -i -e 's|--cov[^[:space:]]*||g' tox.ini

%build
%{__ospython} setup.py build

%install
%{__ospython} setup.py install --no-compile --root %{buildroot}

%files
%doc README.rst
%license LICENSE
%{python3_sitelib}/%{modname}-%{version}-py%{pybasever}.egg-info/*
%{python3_sitelib}/%{modname}/*.py*
%{python3_sitelib}/%{modname}/__pycache__/*.py*

%changelog
* Tue May 20 2025 Devrim Gunduz <devrim@gunduz.org> - 0.2.3-1PGDG
- Initial packaging for the PostgreSQL RPM repository to support Patroni
  on RHEL 9 and RHEL 8.
