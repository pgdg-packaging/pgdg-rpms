%if 0%{?fedora} && 0%{?fedora} == 45
%global __ospython %{_bindir}/python3.15
%global python3_pkgversion 3.15
%endif
%if 0%{?fedora} && 0%{?fedora} <= 44
%global __ospython %{_bindir}/python3.14
%global python3_pkgversion 3.14
%endif
%if 0%{?rhel} && 0%{?rhel} <= 10
%global	__ospython %{_bindir}/python3.12
%global	python3_pkgversion 3.12
%endif
%if 0%{?amzn} == 2023
%global	__ospython %{_bindir}/python3.13
%global	__python3 %{_bindir}/python3.13
%global	python3_pkgversion 3.13
%endif
%if 0%{?suse_version} == 1500
%global	__ospython %{_bindir}/python3.11
%global	python3_pkgversion 311
%endif
%if 0%{?suse_version} == 1600
%global	__ospython %{_bindir}/python3.13
%global	python3_pkgversion 313
%endif

%global	modname matplotlib

Name:		python%{python3_pkgversion}-%{modname}
Version:	3.9.4
Release:	1PGDG%{?dist}
Summary:	Python 2D plotting library

License:	PSF-2.0 AND MIT AND CC0-1.0 AND OFL-1.1 AND Bitstream-Vera AND Public-Domain
URL:		https://matplotlib.org/
Source0:	https://files.pythonhosted.org/packages/source/m/%{modname}/%{modname}-%{version}.tar.gz

BuildRequires:	python%{python3_pkgversion}-devel
BuildRequires:	python%{python3_pkgversion}-pip
BuildRequires:	python%{python3_pkgversion}-meson-python >= 0.13.1
BuildRequires:	python%{python3_pkgversion}-pybind11 >= 2.6
BuildRequires:	python%{python3_pkgversion}-setuptools_scm >= 7
BuildRequires:	python%{python3_pkgversion}-numpy >= 2.0.0
BuildRequires:	gcc gcc-c++ ninja-build pkgconfig
BuildRequires:	freetype-devel qhull-devel

Requires:	python%{python3_pkgversion}-contourpy >= 1.0.1
Requires:	python%{python3_pkgversion}-cycler >= 0.10
Requires:	python%{python3_pkgversion}-dateutil >= 2.7
Requires:	python%{python3_pkgversion}-fonttools >= 4.22.0
Requires:	python%{python3_pkgversion}-kiwisolver >= 1.3.1
Requires:	python%{python3_pkgversion}-numpy >= 1.23
Requires:	python%{python3_pkgversion}-packaging >= 20.0
Requires:	python%{python3_pkgversion}-pillow >= 8
Requires:	python%{python3_pkgversion}-pyparsing >= 2.3.1

%description
Matplotlib is a Python 2D plotting library which produces publication
quality figures in a variety of hardcopy formats and interactive
environments across platforms.

%prep
%autosetup -n %{modname}-%{version}

# meson.build runs "python3 -m setuptools_scm" to get the version, which is
# the OS Python on Amazon Linux 2023, without setuptools_scm. Use the
# version of this package instead:
sed -i "s|version: run_command(find_program('python3'), '-m', 'setuptools_scm', check: true).stdout().strip(),|version: '%{version}',|" meson.build
grep -q "version: '%{version}'," meson.build

%build
export PKG_CONFIG_PATH=$(%{__python3} -m pybind11 --pkgconfigdir)
%pyproject_wheel -C setup-args=-Dsystem-freetype=true -C setup-args=-Dsystem-qhull=true

%install
%pyproject_install

%files
%license LICENSE/*
%doc README.md
%{python3_sitearch}/%{modname}/
%{python3_sitearch}/mpl_toolkits/
%{python3_sitearch}/pylab.py
%{python3_sitearch}/__pycache__/pylab.*
%{python3_sitearch}/%{modname}-%{version}.dist-info/

%changelog
* Tue Oct 06 2026 Devrim Gunduz <devrim@gunduz.org> - 3.9.4-1PGDG
- Initial packaging for the PostgreSQL RPM repository, to satisfy
  pg_statviz dependency on Amazon Linux 2023.
