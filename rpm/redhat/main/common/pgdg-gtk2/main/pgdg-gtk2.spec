%global		sname gtk2
%global		bin_version 2.10.0
# Versionless prefix from pgdg-srpm-macros, per
# https://github.com/pgdg-packaging/pgdg-rpms/issues/28
%global		gtk2instdir %{pgdg_gtk2instdir}

# The libraries are found through the rpath only (there is no ld.so.conf.d
# file), so they must not satisfy the dependencies of OS or EPEL packages,
# and our packages must not pick the EPEL GTK 2. Consumers require
# pgdg-gtk2 by name instead:
%global		__provides_exclude_from ^%{gtk2instdir}/
%global		__requires_exclude ^lib(gtk-x11-2\\.0|gdk-x11-2\\.0|gailutil)\\.so

Name:		pgdg-%{sname}
Version:	2.24.33
Release:	1PGDG%{?dist}
Summary:	GTK+ graphical user interface library, version 2
License:	LGPL-2.0-or-later
URL:		http://www.gtk.org
Source0:	https://download.gnome.org/sources/gtk+/2.24/gtk+-%{version}.tar.xz
# From the Fedora package:
Patch2:		icon-padding.patch
Patch8:		tooltip-positioning.patch
Patch15:	window-dragging.patch
Patch16:	gtk2-c99.patch
Patch17:	gtk2-c89.patch
Patch18:	gtk2-c89-2.patch
Patch19:	gtk2-c89-3.patch
Patch20:	gtk2-c89-4.patch
Patch21:	gtk2-c89-5.patch
Patch22:	gtk2-c89-6.patch

BuildRequires:	pgdg-srpm-macros >= 2.1.0
BuildRequires:	autoconf automake gcc gettext libtool make pkgconfig
BuildRequires:	cups-devel python3-devel
BuildRequires:	pkgconfig(atk) pkgconfig(cairo) pkgconfig(gdk-pixbuf-2.0)
BuildRequires:	pkgconfig(glib-2.0) pkgconfig(pango)
BuildRequires:	pkgconfig(xcomposite) pkgconfig(xcursor) pkgconfig(xdamage)
BuildRequires:	pkgconfig(xfixes) pkgconfig(xi) pkgconfig(xinerama)
BuildRequires:	pkgconfig(xrandr) pkgconfig(xrender)
Requires:	hicolor-icon-theme

%description
GTK+ is a multi-platform toolkit for creating graphical user
interfaces. Offering a complete set of widgets, GTK+ is suitable for
projects ranging from small one-off tools to complete application
suites.

This package installs GTK+ 2 under %{gtk2instdir}, for the packages in the
PostgreSQL RPM repository (the PostGIS shapefile loader GUI), as RHEL 10
does not ship it.

%package devel
Summary:	Development files for GTK+ 2
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	atk-devel cairo-devel gdk-pixbuf2-devel glib2-devel pango-devel
Requires:	libX11-devel libXcomposite-devel libXcursor-devel libXext-devel
Requires:	libXfixes-devel libXi-devel libXinerama-devel libXrandr-devel

%description devel
This package contains the libraries and header files that are needed for
writing applications with version 2 of the GTK+ widget toolkit.

%prep
%autosetup -n gtk+-%{version} -p1

%build
export CFLAGS='%{optflags} -fno-strict-aliasing -std=gnu99'
export LDFLAGS="%{build_ldflags} -Wl,-rpath,%{gtk2instdir}/lib64"
%configure \
	--prefix=%{gtk2instdir} --exec-prefix=%{gtk2instdir} \
	--bindir=%{gtk2instdir}/bin --libdir=%{gtk2instdir}/lib64 \
	--includedir=%{gtk2instdir}/include --datadir=%{gtk2instdir}/share \
	--sysconfdir=%{gtk2instdir}/etc --mandir=%{gtk2instdir}/share/man \
	--with-xinput=xfree --disable-gtk-doc --disable-man \
	--disable-introspection --disable-static
# fight unused direct deps
sed -i -e 's/ -shared / -Wl,-O1,--as-needed\0/g' libtool
%make_build

%install
%make_install
find %{buildroot} -name '*.la' -delete
sed -i '1s|^#!.*python.*$|#!%{__python3}|' %{buildroot}%{gtk2instdir}/bin/gtk-builder-convert
# The immodules cache is created in %%post:
touch %{buildroot}%{gtk2instdir}/lib64/gtk-2.0/%{bin_version}/immodules.cache
# gtk-update-icon-cache and the demo are not needed under this prefix:
%{__rm} -f %{buildroot}%{gtk2instdir}/bin/gtk-update-icon-cache %{buildroot}%{gtk2instdir}/bin/gtk-demo
%{__rm} -rf %{buildroot}%{gtk2instdir}/share/gtk-2.0/demo %{buildroot}%{gtk2instdir}/share/gtk-doc
%find_lang gtk20
%find_lang gtk20-properties
cat gtk20.lang gtk20-properties.lang > all.lang

%post
%{gtk2instdir}/bin/gtk-query-immodules-2.0 --update-cache || :

%files -f all.lang
%license COPYING
%doc AUTHORS NEWS README
%dir %{gtk2instdir}
%{gtk2instdir}/bin/gtk-query-immodules-2.0
%{gtk2instdir}/etc/
%dir %{gtk2instdir}/lib64
%{gtk2instdir}/lib64/libgtk-x11-2.0.so.*
%{gtk2instdir}/lib64/libgdk-x11-2.0.so.*
%{gtk2instdir}/lib64/libgailutil.so.*
%dir %{gtk2instdir}/lib64/gtk-2.0
%dir %{gtk2instdir}/lib64/gtk-2.0/%{bin_version}
%{gtk2instdir}/lib64/gtk-2.0/%{bin_version}/engines/
%{gtk2instdir}/lib64/gtk-2.0/%{bin_version}/immodules/
%{gtk2instdir}/lib64/gtk-2.0/%{bin_version}/printbackends/
%ghost %{gtk2instdir}/lib64/gtk-2.0/%{bin_version}/immodules.cache
%{gtk2instdir}/lib64/gtk-2.0/modules/
%dir %{gtk2instdir}/share
%{gtk2instdir}/share/themes/

%files devel
%{gtk2instdir}/bin/gtk-builder-convert
%{gtk2instdir}/include/
%{gtk2instdir}/lib64/gtk-2.0/include/
%{gtk2instdir}/lib64/lib*.so
%{gtk2instdir}/lib64/pkgconfig/
%{gtk2instdir}/share/aclocal/
%{gtk2instdir}/share/gtk-2.0/

%changelog
* Wed Oct 21 2026 Devrim Gunduz <devrim@gunduz.org> - 2.24.33-1PGDG
- Initial packaging for the PostgreSQL RPM repository, installed under
  /usr/pgdg-gtk2, for the PostGIS shapefile loader GUI on RHEL 10, which
  does not ship GTK+ 2. Based on the Fedora spec file. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/422
