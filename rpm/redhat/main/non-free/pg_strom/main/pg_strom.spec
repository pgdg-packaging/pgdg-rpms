%global debug_package %{nil}
%global	sname	pg_strom
%global __cuda_major_version 12
%global __cuda_minor_version 2
%global __cuda_path	/usr/local/cuda-%{__cuda_major_version}.%{__cuda_minor_version}
%global __systemd_conf	%{_sysconfdir}/systemd/system/postgresql-%%{pgmajorversion}.service.d/%{sname}.conf

%{!?llvm:%global llvm 1}

Name:		%{sname}_%{pgmajorversion}
Version:	6.0
Release:	1PGDG%{?dist}
Summary:	PG-Strom extension module for PostgreSQL
License:	PostgreSQL
URL:		https://github.com/heterodb/pg-strom
Source0:	https://github.com/heterodb/pg-strom/archive/v%{version}.tar.gz
Source1:	systemd-%{sname}.conf
BuildRequires:	postgresql%{pgmajorversion}
BuildRequires:	postgresql%{pgmajorversion}-devel
BuildRequires:	cuda >= %{__cuda_major_version}.%{__cuda_minor_version}
BuildRequires:	nvidia-driver-cuda-libs
Requires:	nvidia-driver-cuda-libs
Requires:	cuda >= %{__cuda_major_version}.%{__cuda_minor_version}
Requires:	postgresql%{pgmajorversion}-server
Requires:	/sbin/ldconfig
# for /sbin/ldconfig
Requires(post):		glibc
Requires(postun):	glibc

%description
PG-Strom is an extension for PostgreSQL database. It is designed to accelerate
mostly batch and analytics workloads with utilization of GPU and NVME-SSD, and
Apache Arrow columnar.

By utilization of GPU (Graphic Processor Unit) device which has thousands
cores per chip, it enables to accelerate SQL workloads for data analytics or
batch processing to big data set.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for pg_strom
Requires:	%{name}%{?_isa} = %{version}-%{release}
%if 0%{?suse_version} >= 1500
BuildRequires:	llvm17-devel clang17-devel
Requires:	llvm17
%endif
%if 0%{?fedora} || 0%{?rhel} >= 8
BuildRequires:	llvm-devel >= 17.0 clang-devel >= 17.0
Requires:	llvm => 17.0
%endif

%description llvmjit
This package provides JIT support for pg_strom
%endif

%prep
%setup -q -n pg-strom-%{version}

%build
export PG_CONFIG=%{pginstdir}/bin/pg_config
export CUDA_PATH=%{__cuda_path}

%{__make} -C src %{?_smp_mflags}

%{__make} -C arrow-tools DESTDIR=%{buildroot} PREFIX=%{pginstdir} arrow2csv
%{__make} -C arrow-tools DESTDIR=%{buildroot} PREFIX=%{pginstdir} pg2arrow

%install
export PG_CONFIG=%{pginstdir}/bin/pg_config
export CUDA_PATH=%{__cuda_path}

%{__rm} -rf %{buildroot}
%{__make} -C src DESTDIR=%{buildroot} install
%{__install} -Dpm 644 %{SOURCE1} %{buildroot}/%{__systemd_conf}

%{__make} -C arrow-tools DESTDIR=%{buildroot} PREFIX=%{pginstdir} install-arrow2csv
%{__make} -C arrow-tools DESTDIR=%{buildroot} PREFIX=%{pginstdir} install-pg2arrow

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc LICENSE README.md
%{pginstdir}/bin/arrow2csv
%{pginstdir}/bin/pg2arrow
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}.control
%{pginstdir}/share/%{sname}/*
%config %{__systemd_conf}

%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/%{sname}*.bc
   %{pginstdir}/lib/bitcode/%{sname}/*.bc
%endif

%changelog
* Mon Mar 31 2025 Devrim Gündüz <devrim@gunduz.org> - 6.0-1PGDG
- Update to 6.0 per changes described at:
  https://heterodb.github.io/pg-strom/release_v6.0/

* Mon Feb 24 2025 Devrim Gündüz <devrim@gunduz.org> - 5.2.2-3PGDG
- Fix Cuda dependency names

* Thu Feb 13 2025 Devrim Gündüz <devrim@gunduz.org> - 5.2.2-2PGDG
- Update LLVM dependencies
- Improve package description

* Fri Aug 2 2024 Devrim Gündüz <devrim@gunduz.org> - 5.2.2-1PGDG
- Update to 5.2.2
- Update Cuda dependency to 12.6

* Fri May 3 2024 Devrim Gündüz <devrim@gunduz.org> - 5.1.2-1PGDG
- Update to 5.1.2

* Wed May 1 2024 Devrim Gündüz <devrim@gunduz.org> - 5.1.1-1PGDG
- Update to 5.1-1
- Add arrow2csv and pg2arrow binaries. Per report from KaiGai Kohei.
- Update Cuda dependency to 12.4

* Sun Mar 3 2024 Devrim Gündüz <devrim@gunduz.org> - 5.1-1PGDG
- Update to 5.1

* Wed Feb 21 2024 Devrim Gündüz <devrim@gunduz.org> - 5.0.3-1PGDG
- Update to 5.0-3

* Sat Jan 20 2024 Devrim Gündüz <devrim@gunduz.org> - 5.0.2-1PGDG
- Update to 5.0-2
- Update Cuda dependency to 12.3

* Mon Dec 18 2023 Devrim Gündüz <devrim@gunduz.org> - 5.0-1PGDG
- Update to 5.0
- Add PGDG branding

* Fri May 19 2023 Devrim Gündüz <devrim@gunduz.org> - 5.0_alpha1-1
- Update to 5.0 alpha1
- Split llvmjit subpackage

* Mon Apr 24 2023 Devrim Gündüz <devrim@gunduz.org> - 3.5-1
- Update to 3.5

* Wed Jan 4 2023 Devrim Gündüz <devrim@gunduz.org> - 3.4-1
- Update to 3.4

* Thu Dec 16 2021 Devrim Gündüz <devrim@gunduz.org> - 3.3-2-1
- Update to 3.3-2

* Tue Oct 19 2021 Devrim Gündüz <devrim@gunduz.org> - 3.2-1
- Update to 3.2

* Thu Aug 26 2021 Devrim Gündüz <devrim@gunduz.org> - 3.1-1
- Update to 3.1

* Tue Oct 27 2020 Devrim Gündüz <devrim@gunduz.org> - 2.3-2
- Use underscore before PostgreSQL version number for consistency, per:
  https://www.postgresql.org/message-id/CAD%2BGXYMfbMnq3c-eYBRULC3nZ-W69uQ1ww8_0RQtJzoZZzp6ug%40mail.gmail.com

* Mon Jun 15 2020 Devrim Gündüz <devrim@gunduz.org> - 2.3-1
- Update to 2.3
- Use Cuda 11

* Thu Dec 19 2019 Devrim Gündüz <devrim@gunduz.org> - 2.2-2
- Initial packaging for the PostgreSQL RPM repository,
  based on KaiGai's spec file
