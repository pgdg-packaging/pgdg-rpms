%pgdg_python3_setup

%global	modname matplotlib

Name:		python%{python3_pkgversion}-%{modname}
Version:	3.9.4
Release:	44PGDG%{?dist}
Summary:	Python 2D plotting library

License:	PSF-2.0 AND MIT AND CC0-1.0 AND OFL-1.1 AND Bitstream-Vera AND Public-Domain
URL:		https://matplotlib.org/
Source0:	https://files.pythonhosted.org/packages/source/m/%{modname}/%{modname}-%{version}.tar.gz

BuildRequires:	python%{python3_pkgversion}-devel
%if ! 0%{?suse_version}
BuildRequires:	pyproject-rpm-macros
%endif
BuildRequires:	python%{python3_pkgversion}-pip
BuildRequires:	python%{python3_pkgversion}-meson-python >= 0.13.1
BuildRequires:	python%{python3_pkgversion}-pybind11 >= 2.6
BuildRequires:	python%{python3_pkgversion}-setuptools_scm >= 7
# RHEL 9 and 10 have numpy 1.x:
%if 0%{?rhel} >= 9
BuildRequires:	python%{python3_pkgversion}-numpy
%else
BuildRequires:	python%{python3_pkgversion}-numpy >= 2.0.0
%endif
BuildRequires:	gcc gcc-c++ ninja-build pkgconfig
BuildRequires:	freetype-devel
# RHEL 10 has no qhull; use ours, found through the rpath:
%if 0%{?rhel} >= 10
BuildRequires:	pgdg-qhull-devel pgdg-srpm-macros >= 2.1.0
Requires:	pgdg-qhull%{?_isa}
%global __requires_exclude ^libqhull_r\\.so
%else
BuildRequires:	qhull-devel
%endif

Requires:	python%{python3_pkgversion}-contourpy >= 1.0.1
Requires:	python%{python3_pkgversion}-cycler >= 0.10
Requires:	python%{python3_pkgversion}-dateutil >= 2.7
Requires:	python%{python3_pkgversion}-fonttools >= 4.22.0
Requires:	python%{python3_pkgversion}-kiwisolver >= 1.3.1
Requires:	python%{python3_pkgversion}-numpy >= 1.23
Requires:	python%{python3_pkgversion}-packaging >= 20.0
Requires:	python%{python3_pkgversion}-pillow >= 8
Requires:	python%{python3_pkgversion}-pyparsing >= 2.3.1

%if 0%{?rhel} == 10
# Replace the EPEL package of the same module, which has the same files:
Obsoletes:	python3-matplotlib < %{version}-%{release}
# EPEL splits these out into subpackages that require its own
# python3-matplotlib version, which would block the updates. This package
# has their files:
Provides:	python3-matplotlib-data = %{version}-%{release}
Obsoletes:	python3-matplotlib-data < %{version}-%{release}
Provides:	python3-matplotlib-data-fonts = %{version}-%{release}
Obsoletes:	python3-matplotlib-data-fonts < %{version}-%{release}
Provides:	python3-matplotlib-gtk3 = %{version}-%{release}
Obsoletes:	python3-matplotlib-gtk3 < %{version}-%{release}
Provides:	python3-matplotlib-gtk4 = %{version}-%{release}
Obsoletes:	python3-matplotlib-gtk4 < %{version}-%{release}
Provides:	python3-matplotlib-qt6 = %{version}-%{release}
Obsoletes:	python3-matplotlib-qt6 < %{version}-%{release}
# We do not build the documentation and the test data:
Obsoletes:	python3-matplotlib-doc < %{version}-%{release}
Obsoletes:	python3-matplotlib-test-data < %{version}-%{release}
%endif

%description
Matplotlib is a Python 2D plotting library which produces publication
quality figures in a variety of hardcopy formats and interactive
environments across platforms.

%if 0%{?rhel} == 10
%package tk
Summary:	Tk backends for matplotlib
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	python%{python3_pkgversion}-pillow-tk
Requires:	python3-tkinter
# Replace the EPEL subpackage, which has the same files:
Provides:	python3-matplotlib-tk = %{version}-%{release}
Provides:	python3-matplotlib-tk%{?_isa} = %{version}-%{release}
Obsoletes:	python3-matplotlib-tk < %{version}-%{release}

%description tk
The Tk backends (TkAgg and TkCairo) for matplotlib.
%endif

%prep
%autosetup -n %{modname}-%{version}

# meson.build runs "python3 -m setuptools_scm" to get the version, which is
# the OS Python on Amazon Linux 2023, without setuptools_scm. Use the
# version of this package instead:
sed -i "s|version: run_command(find_program('python3'), '-m', 'setuptools_scm', check: true).stdout().strip(),|version: '%{version}',|" meson.build
grep -q "version: '%{version}'," meson.build

%build
export PKG_CONFIG_PATH=$(%{__python3} -m pybind11 --pkgconfigdir)
%if 0%{?rhel} >= 10
export PKG_CONFIG_PATH=$PKG_CONFIG_PATH:%{pgdg_qhullinstdir}/lib64/pkgconfig
export CFLAGS="%{build_cflags} -I%{pgdg_qhullinstdir}/include"
export CXXFLAGS="%{build_cxxflags} -I%{pgdg_qhullinstdir}/include"
export LDFLAGS="%{build_ldflags} -L%{pgdg_qhullinstdir}/lib64 -Wl,-rpath,%{pgdg_qhullinstdir}/lib64"
%endif
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
%if 0%{?rhel} == 10
%exclude %{python3_sitearch}/%{modname}/backends/_backend_tk.py
%exclude %{python3_sitearch}/%{modname}/backends/backend_tkagg.py
%exclude %{python3_sitearch}/%{modname}/backends/backend_tkcairo.py
%exclude %{python3_sitearch}/%{modname}/backends/_tkagg.*
%exclude %{python3_sitearch}/%{modname}/backends/__pycache__/_backend_tk.*
%exclude %{python3_sitearch}/%{modname}/backends/__pycache__/backend_tkagg.*
%exclude %{python3_sitearch}/%{modname}/backends/__pycache__/backend_tkcairo.*

%files tk
%{python3_sitearch}/%{modname}/backends/_backend_tk.py
%{python3_sitearch}/%{modname}/backends/backend_tkagg.py
%{python3_sitearch}/%{modname}/backends/backend_tkcairo.py
%{python3_sitearch}/%{modname}/backends/_tkagg.*
%{python3_sitearch}/%{modname}/backends/__pycache__/_backend_tk.*
%{python3_sitearch}/%{modname}/backends/__pycache__/backend_tkagg.*
%{python3_sitearch}/%{modname}/backends/__pycache__/backend_tkcairo.*
%endif

%changelog
* Wed Oct 28 2026 Devrim Gunduz <devrim@gunduz.org> - 3.9.4-44PGDG
- Use %%pgdg_python3_setup from pgdg-srpm-macros 2.5.0 instead of the
  per-distro Python block and the __ospython macro. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/462

* Mon Oct 26 2026 Devrim Gunduz <devrim@gunduz.org> - 3.9.4-43PGDG
- RHEL 10: Move the Tk backends into a new -tk subpackage, which requires
  python3-tkinter and replaces EPEL's python3-matplotlib-tk. Provide and
  obsolete EPEL's -data, -data-fonts, -gtk3, -gtk4 and -qt6 subpackages,
  whose files this package has, and obsolete its -doc and -test-data
  subpackages. They require EPEL's own python3-matplotlib version, so they
  made dnf upgrade fail. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/422

* Sat Oct 24 2026 Devrim Gunduz <devrim@gunduz.org> - 3.9.4-42PGDG
- Add RHEL 10 support, without EPEL: build against numpy 1.26 from RHEL, as
  on RHEL 9, and against pgdg-qhull, found through the rpath.
- RHEL 10: Obsolete the EPEL python3-matplotlib package. Start the release
  from 42, so that our packages win over EPEL's. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/422

* Tue Oct 06 2026 Devrim Gunduz <devrim@gunduz.org> - 3.9.4-1PGDG
- Initial packaging for the PostgreSQL RPM repository, to satisfy
  pg_statviz dependency on Amazon Linux 2023.
- Add RHEL 9 support (python3.12), for pg_statviz. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/249
