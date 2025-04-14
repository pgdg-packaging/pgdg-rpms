%if 0%{?fedora} >= 40 || 0%{?rhel} >= 10
%{expand: %%global py3ver %(echo `%{__python3} -c "import sys; sys.stdout.write(sys.version[:4])"`)}
%else
%{expand: %%global py3ver %(echo `%{__python3} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%endif

%global sname check_patroni

Name:		nagios-plugins-patroni
Version:	2.2.0
Release:	1PGDG%{dist}
Summary:	Patroni monitoring plugin for Nagios
License:	PostgreSQL
Url:		https://github.com/dalibo/%{sname}/
Source0:	https://github.com/dalibo/%{sname}/archive/refs/tags/v%{version}.tar.gz
BuildArch:	noarch
Requires:	nagios-plugins
Provides:	%{sname} = %{version}

%description
check_patroni is a monitoring plugin of patroni for Nagios.

%prep
%setup -q -n %{sname}-%{version}

%build
%{__python3} setup.py build

%install
%{__python3} setup.py install --no-compile --root %{buildroot}

%files
%defattr(-,root,root,0755)
%doc docs
%license LICENSE
%{_bindir}/%{sname}
%{python3_sitelib}/%{sname}/*.py
%{python3_sitelib}/%{sname}-%{version}-py%{py3ver}.egg-info
%{python3_sitelib}/%{sname}/__pycache__/*.pyc

%changelog
* Sun Apr 13 2025 Devrim Gündüz <devrim@gunduz.org> 2.2.0-1PGDG
- Initial packaging for the PostgreSQL RPM repository
