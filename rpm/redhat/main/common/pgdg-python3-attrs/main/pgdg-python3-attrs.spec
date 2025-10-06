%global pypi_name attrs
%global sname attr
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

Name:		python%{python3_pkgversion}-attrs
Version:	22.1.0
Release:	42PGDG%{?dist}
Summary:	Python attributes without boilerplate

License:	MIT
URL:		https://www.attrs.org/
BuildArch:	noarch
Source0:	https://github.com/hynek/%{pypi_name}/archive/%{version}/%{pypi_name}-%{version}.tar.gz

BuildRequires:	python%{python3_pkgversion}-devel python%{python3_pkgversion}-setuptools
Requires:	python%{python3_pkgversion}


%description
attrs is an MIT-licensed Python package with class decorators that
ease the chores of implementing the most common attribute-related
object protocols.

%prep
%setup -q -n %{pypi_name}-%{version}

%build
%{__ospython} setup.py build

%install
%{__ospython} setup.py install -O1 --skip-build --root %{buildroot}

%files
%license LICENSE
%doc AUTHORS.rst README.rst
%{python3_sitelib}/%{sname}/*.py*
%{python3_sitelib}/%{sname}/py.typed
%{python3_sitelib}/%{sname}/__pycache__/*.pyc
%{python3_sitelib}/%{pypi_name}/*.py*
%{python3_sitelib}/%{pypi_name}/py.typed
%{python3_sitelib}/%{pypi_name}/__pycache__/*.pyc
%{python3_sitelib}/%{pypi_name}-%{version}-py%{pyver}.egg-info

%changelog
* Mon Oct 6 2025 Devrim Gunduz <devrim@gunduz.org> - 22.1.0-42PGDG
- Initial packaging for the PostgreSQL RPM repository to satisfy
  pg_activity dependency. Package is for RHEL 8 only.
