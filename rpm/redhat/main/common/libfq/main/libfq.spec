Summary:	A wrapper library for the Firebird C API
Name:		libfq
Version:	0.6.1
Release:	2PGDG%{dist}
Source:		https://github.com/ibarwick/%{name}/archive/%{version}.tar.gz
Patch0:		%{name}-c23.patch
URL:		https://github.com/ibarwick/%{name}
License:	PostgreSQL
BuildRequires:	firebird-devel

BuildRequires:	libfbclient2
Requires:	libfbclient2

%description
A wrapper library for the Firebird C API, loosely based on libpq for PostgreSQL.

%prep
%setup -q -n %{name}-%{version}
%patch -P 0 -p1

%build
%configure --prefix=%{_prefix} \
	--with-ibase=%{_includedir}/firebird --libdir=%{_libdir}/

%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__make} %{?_smp_mflags} DESTDIR=%{buildroot} install
%{__rm} %{buildroot}%{_libdir}/%{name}.la

%files
%defattr(-, root, root)
%{_libdir}/%{name}.a
%{_libdir}/%{name}.so
%{_libdir}/%{name}-%version.so
%{_includedir}/%{name}-expbuffer.h
%{_includedir}/%{name}-version.h
%{_includedir}/%{name}.h

%changelog
* Mon May 5 2025 Devrim Gündüz <devrim@gunduz.org> - 0.6.1-2PGDG
- Remove RHEL 7 support

* Thu May 23 2024 Devrim Gündüz <devrim@gunduz.org> - 0.6.1-1PGDG
- Update to 0.6.1 per changes described at:
  https://github.com/ibarwick/libfq/releases/tag/0.6.1
  https://github.com/ibarwick/libfq/releases/tag/0.6.0
- Remove patch added in 0.5.0-3

* Thu Apr 25 2024 Devrim Gündüz <devrim@gunduz.org> - 0.5.0-3PGDG
- Add a temp patch to fix build issues on Fedora 40.

* Sun Feb 18 2024 Devrim Gündüz <devrim@gunduz.org> - 0.5.0-2PGDG
- Add PGDG branding
- Fix rpmlint warning

* Sun Jan 1 2023 Devrim Gündüz <devrim@gunduz.org> - 0.5.0-1
- Update to 0.5.0

* Tue Dec 6 2022 Devrim Gündüz <devrim@gunduz.org> - 0.4.3-3
- Remove Advance Toolchain support from RHEL 7 - ppc64le.

* Wed Oct 19 2022 Devrim Gündüz <devrim@gunduz.org> - 0.4.3-2
- Remove .la file, per
  https://fedoraproject.org/wiki/Changes/RemoveLaFiles

* Mon Feb 21 2022 Devrim Gündüz <devrim@gunduz.org> - 0.4.3-1
- Update to 0.4.3

* Tue Oct 20 2020 Devrim Gündüz <devrim@gunduz.org> - 0.4.2-1
- Initial packaging for the PostgreSQL RPM repository, to satisfy
  firebird_fdw dependency. This is an improved version of the upstream
  spec file.
