%global		sname libimagequant
# Versionless prefix from pgdg-srpm-macros, per
# https://github.com/pgdg-packaging/pgdg-rpms/issues/28
%global		libimagequantinstdir %{pgdg_libimagequantinstdir}

# The library is found through the rpath only (there is no ld.so.conf.d
# file), so it must not satisfy the dependencies of OS or EPEL packages,
# and our packages must not pick the EPEL libimagequant. Consumers require
# pgdg-libimagequant by name instead:
%global		__provides_exclude_from ^%{libimagequantinstdir}/
%global		__requires_exclude ^libimagequant\\.so

Name:		pgdg-%{sname}
# 2.18.0 is the last release of the C library; 4.x is written in Rust.
Version:	2.18.0
Release:	1PGDG%{?dist}
Summary:	Palette quantization library
License:	GPL-3.0-or-later AND HPND
URL:		https://pngquant.org/lib/
Source0:	https://github.com/ImageOptim/%{sname}/archive/refs/tags/%{version}.tar.gz#/%{sname}-%{version}.tar.gz

BuildRequires:	pgdg-srpm-macros >= 2.4.0
BuildRequires:	gcc make

%description
Small, portable C library for high-quality conversion of RGBA images to
8-bit indexed-color (palette) images.

This package installs libimagequant under %{libimagequantinstdir}, for the
packages in the PostgreSQL RPM repository.

%package devel
Summary:	Development files for %{sname}
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{sname}.

%prep
%setup -q -n %{sname}-%{version}

%build
# Not an autoconf script: it only takes the options below.
./configure \
	--prefix=%{libimagequantinstdir} \
	--with-openmp \
	--extra-cflags="%{build_cflags}" \
	--extra-ldflags="%{build_ldflags}"
%{make_build}

%install
%{make_install}
%{__rm} -f %{buildroot}%{libimagequantinstdir}/lib/%{sname}.a

%files
%license COPYRIGHT
%doc CHANGELOG README.md
%dir %{libimagequantinstdir}
%dir %{libimagequantinstdir}/lib
%{libimagequantinstdir}/lib/%{sname}.so.0

%files devel
%{libimagequantinstdir}/include/
%{libimagequantinstdir}/lib/%{sname}.so
%{libimagequantinstdir}/lib/pkgconfig/

%changelog
* Sat Oct 24 2026 Devrim Gunduz <devrim@gunduz.org> - 2.18.0-1PGDG
- Initial packaging for the PostgreSQL RPM repository, installed under
  /usr/pgdg-libimagequant, so that Pillow does not need the EPEL
  libimagequant package on RHEL 9 and 10. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/422
