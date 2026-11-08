%global		sname gc
%global		gcinstdir /usr/pgdg-%{sname}

# The libraries are found through the rpath only (there is no ld.so.conf.d
# file), so they must not satisfy the dependencies of OS or EPEL packages,
# and our packages must not pick the OS or EPEL libraries. Consumers require
# pgdg-gc by name instead:
%global		__provides_exclude_from ^%{gcinstdir}/
%global		__requires_exclude ^lib(gc|cord|gctba)\\.so

Name:		pgdg-%{sname}
Version:	8.2.12
Release:	1PGDG%{?dist}
Summary:	Boehm-Demers-Weiser conservative garbage collector
License:	Boehm-GC
URL:		https://www.hboehm.info/gc/
Source0:	https://github.com/bdwgc/bdwgc/releases/download/v%{version}/%{sname}-%{version}.tar.gz

BuildRequires:	gcc make

%description
The Boehm-Demers-Weiser conservative garbage collector can be used as a
garbage collecting replacement for C malloc.

This package installs it under %{gcinstdir}, for the packages in the
PostgreSQL RPM repository, as RHEL 10 does not ship it.

%package devel
Summary:	Header files and development libraries for %{name}
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description devel
This package contains the header files and development libraries
for %{name}.

%prep
%setup -q -n %{sname}-%{version}

%build
# see https://bugzilla.redhat.com/689877
CPPFLAGS="-DUSE_GET_STACKBASE_FOR_MAIN $CPPFLAGS"
export CPPFLAGS
# The C++ interface is not built: pgcopydb only uses the C library.
%configure \
	--prefix=%{gcinstdir} \
	--exec-prefix=%{gcinstdir} \
	--libdir=%{gcinstdir}/lib64 \
	--includedir=%{gcinstdir}/include \
	--datarootdir=%{gcinstdir}/share \
	--disable-dependency-tracking \
	--disable-static \
	--disable-docs \
	--enable-large-config \
	--enable-threads=posix
%{__make} %{?_smp_mflags}

%install
%{__make} install DESTDIR=%{buildroot}
%{__rm} -f %{buildroot}%{gcinstdir}/lib64/*.la
%{__rm} -rf %{buildroot}%{gcinstdir}/share

%files
%doc README.md
%dir %{gcinstdir}
%dir %{gcinstdir}/lib64
%{gcinstdir}/lib64/lib*.so.*

%files devel
%doc doc/README.environment doc/README.linux
%{gcinstdir}/include/
%{gcinstdir}/lib64/lib*.so
%{gcinstdir}/lib64/pkgconfig/

%changelog
* Sun Nov 8 2026 Devrim Gunduz <devrim@gunduz.org> - 8.2.12-1PGDG
- Initial packaging for the PostgreSQL RPM repository, installed under
  /usr/pgdg-gc, so that pgcopydb does not need the EPEL gc package on
  RHEL 10. Based on the Fedora spec file. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/513
