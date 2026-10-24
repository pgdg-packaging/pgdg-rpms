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
%if 0%{?rhel} == 9
%global	__python3 %{_bindir}/python3.12
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

%global	modname pillow

Name:		python%{python3_pkgversion}-%{modname}
Version:	13.0.0
Release:	42PGDG%{?dist}
Summary:	Python image processing library

License:	MIT-CMU
URL:		https://python-pillow.github.io/
Source0:	https://files.pythonhosted.org/packages/source/p/%{modname}/%{modname}-%{version}.tar.gz

BuildRequires:	python%{python3_pkgversion}-devel
%if ! 0%{?suse_version}
BuildRequires:	pyproject-rpm-macros
%endif
BuildRequires:	python%{python3_pkgversion}-pip
BuildRequires:	python%{python3_pkgversion}-setuptools >= 67.8
BuildRequires:	python%{python3_pkgversion}-wheel
BuildRequires:	gcc
BuildRequires:	freetype-devel lcms2-devel libjpeg-turbo-devel
# On RHEL, libimagequant comes from pgdg-libimagequant (EPEL is not needed),
# which is found through the rpath:
%if 0%{?rhel}
BuildRequires:	pgdg-srpm-macros >= 2.4.0 pgdg-libimagequant-devel
Requires:	pgdg-libimagequant%{?_isa}
%global __requires_exclude ^libimagequant\\.so
%else
BuildRequires:	libimagequant-devel
%endif
BuildRequires:	libtiff-devel libwebp-devel libxcb-devel openjpeg2-devel zlib-devel

%if 0%{?rhel} == 10
# Replace the EPEL package of the same module, which has the same files:
Obsoletes:	python3-pillow < %{version}-%{release}
%endif

%description
Pillow is the friendly PIL fork. PIL is the Python Imaging Library. It adds
image processing capabilities to your Python interpreter, and supports many
file formats.

%prep
%autosetup -n %{modname}-%{version}

# The setuptools of RHEL 9 (68) and Amazon Linux 2023 (69) supports neither
# PEP 639 license strings nor license-files (setuptools >= 77 does), so use
# the old license table. pybind11 is only used for its ParallelCompile helper,
# which RHEL 9 does not have for python3.12, so drop it. Also drop the
# Python 3.15 classifier, which older trove-classifiers reject.
sed -i -e 's/^license = "MIT-CMU"/license = { text = "MIT-CMU" }/' \
	-e '/^license-files = /d' \
	-e 's/"setuptools>=77"/"setuptools>=67.8"/' \
	-e '/^  "pybind11",$/d' \
	-e '/"Programming Language :: Python :: 3.15",/d' pyproject.toml
sed -i -e '/^from pybind11.setup_helpers import ParallelCompile$/d' \
	-e '/^ParallelCompile(/d' setup.py

%build
%if 0%{?rhel}
export IMAGEQUANT_ROOT=%{pgdg_libimagequantinstdir}
export LDFLAGS="%{build_ldflags} -Wl,-rpath,%{pgdg_libimagequantinstdir}/lib"
%pyproject_wheel -C imagequant=enable
%else
%pyproject_wheel
%endif

%install
%pyproject_install

%files
%license LICENSE
%doc README.md
%{python3_sitearch}/PIL/
%{python3_sitearch}/%{modname}-%{version}.dist-info/

%changelog
* Sat Oct 24 2026 Devrim Gunduz <devrim@gunduz.org> - 13.0.0-42PGDG
- RHEL: Build against pgdg-libimagequant, found through the rpath, instead
  of the EPEL libimagequant, and add RHEL 10 support, for pg_statviz.
- RHEL 10: Obsolete the EPEL python3-pillow package. Start the release from
  42, so that our packages win over EPEL's. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/422

* Sun Oct 18 2026 Devrim Gündüz <devrim@gunduz.org> - 13.0.0-1PGDG
- Update to 13.0.0 per changes described at:
  https://github.com/python-pillow/Pillow/releases/tag/13.0.0
- Patch pyproject.toml and setup.py so that it builds with the setuptools
  of RHEL 9 and Amazon Linux 2023, and without pybind11.

* Tue Oct 06 2026 Devrim Gunduz <devrim@gunduz.org> - 11.1.0-1PGDG
- Initial packaging for the PostgreSQL RPM repository, to satisfy
  pg_statviz dependency on Amazon Linux 2023.
- Add RHEL 9 support (python3.12), for pg_statviz. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/249
