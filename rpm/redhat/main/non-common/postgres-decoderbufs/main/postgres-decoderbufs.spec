%global sname postgres-decoderbufs

%{!?llvm:%global llvm 1}

Name:		%{sname}_%{pgmajorversion}
Version:	3.3.0
Release:	1PGDG%{?dist}
Summary:	PostgreSQL Protocol Buffers logical decoder plugin

License:	MIT
URL:		https://github.com/debezium/%{sname}

Source0:	https://github.com/debezium/%{sname}/archive/refs/tags/v%{version}.Final.tar.gz

BuildRequires:	gcc
BuildRequires:	postgresql%{pgmajorversion}-devel
%if 0%{?suse_version} >= 1500
BuildRequires:	libprotobuf-c-devel
Requires:	libprotobuf-c1
%else
BuildRequires:	protobuf-c-devel
Requires:	protobuf-c
%endif

%description
A PostgreSQL logical decoder output plugin to deliver data as Protocol Buffers messages.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for postgres-decoderbufs
Requires:	%{name}%{?_isa} = %{version}-%{release}
%if 0%{?suse_version} == 1500
BuildRequires:	llvm17-devel clang17-devel
Requires:	llvm17
%endif
%if 0%{?suse_version} == 1600
BuildRequires:	llvm19-devel clang19-devel
Requires:	llvm19
%endif
%if 0%{?fedora} || 0%{?rhel} >= 8
BuildRequires:	llvm-devel >= 19.0 clang-devel >= 19.0
Requires:	llvm >= 19.0
%endif

%description llvmjit
This package provides JIT support for postgres-decoderbufs
%endif


%prep
%setup -qn %{sname}-%{version}.Final

%build
PATH=%{pginstdir}/bin/:$PATH %make_build

%install
PATH=%{pginstdir}/bin/:$PATH %make_install

%files
%doc README.md
%license LICENSE
%{pginstdir}/lib/decoderbufs.so
%{pginstdir}/share/extension/decoderbufs.control

%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/decoderbufs*.bc
   %{pginstdir}/lib/bitcode/decoderbufs/src/
%endif

%changelog
* Sun Oct 5 2025 Devrim Gündüz <devrim@gunduz.org> - 3.3.0-1PGDG
- Update to 3.3.0 per changes described at
  https://github.com/debezium/postgres-decoderbufs/releases/tag/v3.3.0.Final
- Add SLES 16 support

* Wed Oct 01 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com> - 3.2.0-2PGDG
- Bump release number (missed in previous commit)

* Tue Sep 30 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com>
- Change => to >= in Requires and BuildRequires

* Sat Jul 19 2025 Devrim Gündüz <devrim@gunduz.org> - 3.2.0-1PGDG
- Update to 3.2.0 per changes described at
  https://github.com/debezium/postgres-decoderbufs/releases/tag/v3.2.0.Final

* Mon Jun 2 2025 Devrim Gündüz <devrim@gunduz.org> - 3.1.1-1PGDG
- Update to 3.1.1 per changes described at
  https://github.com/debezium/postgres-decoderbufs/releases/tag/v3.1.1.Final

* Mon Nov 18 2024 Devrim Gündüz <devrim@gunduz.org> - 3.0.2-1PGDG
- Update to 3.0.2 per changes described at
  https://github.com/debezium/postgres-decoderbufs/releases/tag/v3.0.2.Final

* Mon Oct 28 2024 Devrim Gündüz <devrim@gunduz.org> - 3.0.1-1PGDG
- Update to 3.0.1 per changes described at
  https://github.com/debezium/postgres-decoderbufs/releases/tag/v3.0.1.Final

* Mon Jul 29 2024 Devrim Gündüz <devrim@gunduz.org> - 2.7.0-1PGDG
- Update to 2.7.0 per changes described at
  https://github.com/debezium/postgres-decoderbufs/releases/tag/v2.7.0.Final
- Update LLVM dependencies
- Remove RHEL 7 support

* Thu Apr 25 2024 Devrim Gündüz <devrim@gunduz.org> - 2.6.1-1PGDG
- Update to 2.6.1 per changes described at
  https://github.com/debezium/postgres-decoderbufs/releases/tag/v2.6.1.Final

* Tue Mar 5 2024 Devrim Gündüz <devrim@gunduz.org> - 2.5.2-1PGDG
- Update to 2.5.2 per changes described at
  https://github.com/debezium/postgres-decoderbufs/releases/tag/v2.5.2.Final

* Mon Feb 26 2024 Devrim Gündüz <devrim@gunduz.org> - 2.5.1-1PGDG
- Update to 2.5.1

* Fri Jan 5 2024 Devrim Gündüz <devrim@gunduz.org> - 2.5.0-1PGDG
- Update to 2.5.0

* Wed Dec 6 2023 Devrim Gündüz <devrim@gunduz.org> - 2.4.1-1PGDG
- Update to 2.4.1

* Wed Oct 18 2023 Devrim Gündüz <devrim@gunduz.org> - 2.4.0-1
- Update to 2.4.0
- Add SLES 15 support

* Fri Jul 21 2023 Devrim Gündüz <devrim@gunduz.org> - 2.3.0-1
- Update to 2.3.0
- Add PGDG branding

* Thu May 25 2023 Devrim Gündüz <devrim@gunduz.org> - 2.2.1-1
- Update to 2.2.1

* Mon Apr 24 2023 Devrim Gündüz <devrim@gunduz.org> - 2.2.0-1
- Update to 2.2.0

* Wed Feb 22 2023 Devrim Gündüz <devrim@gunduz.org> - 2.1.2-1
- Update to 2.1.2

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 1.7.0-1
- Update to 1.7.0

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 1.5.2-2
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Wed Jun 2 2021 Devrim Gündüz <devrim@gunduz.org> - 1.5.2-1
- Update to 1.5.2
- Remove pgxs patches, and export PATH instead.

* Thu Jan 7 2021 Devrim Gündüz <devrim@gunduz.org> - 1.3.1-1
- Update to 1.3.1
- Drop PostGIS BR

* Thu Sep 26 2019 Devrim Gündüz <devrim@gunduz.org>
- Rebuild for PostgreSQL 12

* Tue May 14 2019 - Jiri Pechanec <jpechane@redhat.com> 0.9.5-1
- Initial RPM packaging
