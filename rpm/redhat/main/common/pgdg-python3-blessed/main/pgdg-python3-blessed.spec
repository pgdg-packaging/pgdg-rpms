%global	sname blessed

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
%global python3_sitelib %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")

Name:		python%{python3_pkgversion}-%{sname}
Version:	1.22.0
Release:	43PGDG%{?dist}
Summary:	Easy, practical library for making terminal apps, by providing an elegant, well- documented interface to Colors, Keyboard input, and screen Positioning capabilities

License:	MIT
URL:		https://github.com/jquast/%{sname}
Source0:	https://files.pythonhosted.org/packages/source/h/%{sname}/%{sname}-%{version}.tar.gz
BuildArch:	noarch

BuildRequires:	python%{python3_pkgversion}-devel python%{python3_pkgversion}-setuptools
BuildRequires:	python%{python3_pkgversion}-six python%{python3_pkgversion}-wcwidth
Requires:	python%{python3_pkgversion}

%description
Blessed is an easy, practical *library* for making *terminal* apps, by providing
an elegant, well-documented interface to Colors_, Keyboard_ input, and screen
position and Location_ capabilities... code-block:: python from blessed import
Terminal term Terminal() print(term.home + term.clear + term.move_y(term.height
// 2))...

%prep
%autosetup -n %{sname}-%{version}
# Remove bundled egg-info
%{__rm} -rf %{sname}.egg-info

%build
%{__ospython} setup.py build

%install
%{__ospython} setup.py install -O1 --skip-build --root %{buildroot}

%files
%license LICENSE
%doc README.rst
%{python3_sitelib}/%{sname}
%{python3_sitelib}/%{sname}-%{version}-py%{pyver}.egg-info

%changelog
* Mon Oct 6 2025 Devrim Gündüz <devrim@gunduz.org> - 1.22.0-42PGDG
- Update to 1.22.0
- Use more macros and get rid of pypi_source macro.

* Mon Oct 6 2025 Devrim Gündüz <devrim@gunduz.org> - 1.19.1-42PGDG
- Initial packaging for the PostgreSQL RPM repository to satisfy
  pg_activity dependency. Package is for RHEL 8 only.

