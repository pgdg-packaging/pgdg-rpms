%global sname poppler
%global popplerinstdir /usr/%{name}

Summary:	PDF rendering library
Name:		pgdg-%{sname}
Version:	26.08.0
Release:	1%{?dist}
License:	(GPLv2 or GPLv3) and GPLv2+ and LGPLv2+ and MIT
URL:		https://poppler.freedesktop.org/
Source0:	https://poppler.freedesktop.org/poppler-%{version}.tar.xz
Source1:	poppler20-pgdg-libs.conf

# https://bugzilla.redhat.com/show_bug.cgi?id=1185007
Patch0:		poppler-0.30.0-rotated-words-selection.patch

# https://bugzilla.redhat.com/show_bug.cgi?id=1602662
# https://bugzilla.redhat.com/show_bug.cgi?id=1638712
Patch4:		poppler-0.66.0-covscan.patch

# https://bugzilla.redhat.com/show_bug.cgi?id=1618766
Patch21:	poppler-0.66.0-nss.patch

BuildRequires:	cmake gettext-devel
BuildRequires:	pkgconfig(cairo) pkgconfig(cairo-ft)
BuildRequires:	pkgconfig(cairo-pdf) pkgconfig(cairo-ps)
BuildRequires:	pkgconfig(cairo-svg) pkgconfig(fontconfig)
BuildRequires:	pkgconfig(freetype2) pkgconfig(gdk-pixbuf-2.0)
BuildRequires:	pkgconfig(gio-2.0) pkgconfig(gobject-2.0)
BuildRequires:	pkgconfig(gobject-introspection-1.0) pkgconfig(gtk+-3.0)
BuildRequires:	pkgconfig(gtk-doc) pkgconfig(lcms2)
BuildRequires:	pkgconfig(libjpeg) pkgconfig(libopenjp2)
BuildRequires:	pkgconfig(libpng) pkgconfig(libtiff-4)
BuildRequires:	pkgconfig(nss) pkgconfig(pgdg-poppler-data)
BuildRequires:	pkgconfig(Qt5Core) pkgconfig(Qt5Gui)
BuildRequires:	pkgconfig(Qt5Test) pkgconfig(Qt5Widgets)
BuildRequires:	pkgconfig(Qt5Xml) python3-devel

Requires:	pgdg-poppler-data

Obsoletes:	pgdg-poppler-glib-demos < 0.60.1-1

%description
%{name} is a PDF rendering library.

%package devel
Summary:	Libraries and headers for poppler
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description devel
You should install the poppler-devel package if you would like to
compile applications based on poppler.

%package glib
Summary:	Glib wrapper for poppler
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description glib
%{summary}.

%package glib-devel
Summary:	Development files for glib wrapper
Requires:	%{name}-glib%{?_isa} = %{version}-%{release}
Requires:	%{name}-devel%{?_isa} = %{version}-%{release}
Suggests:	%{name}-doc = %{version}-%{release}

%description glib-devel
%{summary}.

%package glib-doc
Summary:	Documentation for glib wrapper
BuildArch:	noarch

%description glib-doc
%{summary}.

%package qt5
Summary:	Qt5 wrapper for poppler
Requires:	%{name}%{?_isa} = %{version}-%{release}
%description qt5
%{summary}.

%package qt5-devel
Summary:	Development files for Qt5 wrapper
Requires:	%{name}-qt5%{?_isa} = %{version}-%{release}
Requires:	%{name}-devel%{?_isa} = %{version}-%{release}
Requires:	qt5-qtbase-devel
%description qt5-devel
%{summary}.

%package cpp
Summary:	Pure C++ wrapper for poppler
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description cpp
%{summary}.

%package cpp-devel
Summary:	Development files for C++ wrapper
Requires:	%{name}-cpp%{?_isa} = %{version}-%{release}
Requires:	%{name}-devel%{?_isa} = %{version}-%{release}

%description cpp-devel
%{summary}.

%package utils
Summary:	Command line utilities for converting PDF files
Requires:	%{name}%{?_isa} = %{version}-%{release}
%description utils
Command line tools for manipulating PDF files and converting them to
other formats.

%prep
%autosetup -p1 -n %{sname}-%{version}
chmod -x poppler/CairoFontEngine.cc

%build
mkdir build
cd build
export CC="gcc -fPIC" # hack to make the cmake call pass
%cmake \
	-DCMAKE_INSTALL_PREFIX=/usr/pgdg-poppler \
	-DENABLE_CMS=lcms2 \
	-DENABLE_DCTDECODER=libjpeg \
	-DENABLE_GTK_DOC=ON \
	-DENABLE_LIBOPENJPEG=openjpeg2 \
	-DENABLE_ZLIB=OFF \
	-DENABLE_NSS=ON \
	-DENABLE_UNSTABLE_API_ABI_HEADERS=ON \
	-DENABLE_QT6=OFF \
	..
unset CC
%{__make} %{?_smp_mflags}

%install
cd build
%{__make} install DESTDIR=$RPM_BUILD_ROOT

# Install linker config file:
%{__mkdir} -p %{buildroot}%{_sysconfdir}/ld.so.conf.d/
%{__install} %{SOURCE1} %{buildroot}%{_sysconfdir}/ld.so.conf.d/

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post glib -p /sbin/ldconfig
%postun glib -p /sbin/ldconfig

%post qt5 -p /sbin/ldconfig
%postun qt5 -p /sbin/ldconfig

%post cpp -p /sbin/ldconfig
%postun cpp -p /sbin/ldconfig

%files
%doc README.md
%license COPYING
%{popplerinstdir}/lib64/libpoppler.so.104*
%config(noreplace) %attr (644,root,root) %{_sysconfdir}/ld.so.conf.d/poppler20-pgdg-libs.conf

%files devel
%{popplerinstdir}/lib64/pkgconfig/poppler.pc
%{popplerinstdir}/lib64/pkgconfig/poppler-*.pc
%{popplerinstdir}/lib64/libpoppler.so
%dir %{popplerinstdir}/include/poppler/
# xpdf headers
%{popplerinstdir}/include/poppler/*.h
%{popplerinstdir}/include/poppler/fofi/
%{popplerinstdir}/include/poppler/goo/
%{popplerinstdir}/include/poppler/splash/

%files glib
%{popplerinstdir}/lib64/libpoppler-glib.so.8*
%{popplerinstdir}/lib64/girepository-1.0/Poppler-0.18.typelib

%files glib-devel
%{popplerinstdir}/lib64/pkgconfig/poppler-glib.pc
%{popplerinstdir}/lib64/libpoppler-glib.so
%{popplerinstdir}/share/gir-1.0/Poppler-0.18.gir
%{popplerinstdir}/include/poppler/glib/

%files glib-doc
%license COPYING
%{popplerinstdir}/share/gtk-doc/

%files qt5
%{popplerinstdir}/lib64/libpoppler-qt5.so.1*

%files qt5-devel
%{popplerinstdir}/lib64/libpoppler-qt5.so
%{popplerinstdir}/lib64/pkgconfig/poppler-qt5.pc
%{popplerinstdir}/include/poppler/qt5/

%files cpp
%{popplerinstdir}/lib64/libpoppler-cpp.so.0*

%files cpp-devel
%{popplerinstdir}/lib64/pkgconfig/poppler-cpp.pc
%{popplerinstdir}/lib64/libpoppler-cpp.so
%{popplerinstdir}/include/poppler/cpp

%files utils
%{popplerinstdir}/bin/pdf*
%{popplerinstdir}/share/man/man1/*

%changelog
* Mon Aug 31 2026 Devrim Gündüz <devrim@gunduz.org> - 26.08.0-1
- Update to 26.08.0 per changes described at:
  https://poppler.freedesktop.org/releases.html

* Wed May 19 2021 Devrim Gündüz <devrim@gunduz.org> - 20.11.0-3
- Add linker config file

* Wed May 19 2021 Devrim Gündüz <devrim@gunduz.org> - 20.11.0-2
- Initial packaging for PostgreSQL RPM repository, to prevent
  further breakages caused by Poppler updates on RHEL 8.x

