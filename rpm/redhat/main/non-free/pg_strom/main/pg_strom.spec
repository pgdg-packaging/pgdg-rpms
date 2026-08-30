%global debug_package %{nil}
%global	sname	pg_strom
%global __cuda_major_version 13
%global __cuda_minor_version 1
%global __cuda_path	/usr/local/cuda-%{__cuda_major_version}.%{__cuda_minor_version}
%global __systemd_conf	%{_sysconfdir}/systemd/system/postgresql-%%{pgmajorversion}.service.d/%{sname}.conf
%global arrowparquetrelver	2300

%{!?llvm:%global llvm 1}

# Propagate %%llvm into the actual build: PGXS decides whether to invoke
# clang/llvm-config based on with_llvm from the installed postgresql*-devel's
# Makefile.global, not from this spec's %%llvm. Without passing with_llvm=no
# through to make, setting %%llvm 0 here only drops the llvm BuildRequires/
# subpackage/files, while the build still tries to run clang regardless.
%if %llvm
%global with_llvm_arg %{nil}
%else
%global with_llvm_arg with_llvm=no
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	6.1
Release:	3PGDG%{?dist}
Summary:	PG-Strom extension module for PostgreSQL
License:	PostgreSQL
URL:		https://github.com/heterodb/pg-strom
Source0:	https://github.com/heterodb/pg-strom/archive/v%{version}.tar.gz
Source1:	systemd-%{sname}.conf
BuildRequires:	arrow-devel parquet-devel
BuildRequires:	postgresql%{pgmajorversion}
BuildRequires:	postgresql%{pgmajorversion}-devel
BuildRequires:	cuda >= %{__cuda_major_version}.%{__cuda_minor_version}
BuildRequires:	nvidia-driver-cuda-libs
Requires:	arrow%{arrowparquetrelver}-libs parquet%{arrowparquetrelver}-libs
Requires:	nvidia-driver-cuda-libs
Requires:	cuda >= %{__cuda_major_version}.%{__cuda_minor_version}
Requires:	postgresql%{pgmajorversion}-server
Requires:	/sbin/ldconfig
Requires:	apache-arrow-release >= 23.0.0
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
This package provides JIT support for pg_strom
%endif

%prep
%setup -q -n pg-strom-%{version}

%build
export PG_CONFIG=%{pginstdir}/bin/pg_config
export CUDA_PATH=%{__cuda_path}

%{__make} -C src %{?_smp_mflags} %{with_llvm_arg}

%{__make} -C arrow-tools DESTDIR=%{buildroot} PREFIX=%{pginstdir} arrow2csv
%{__make} -C arrow-tools DESTDIR=%{buildroot} PREFIX=%{pginstdir} pg2arrow

%install
export PG_CONFIG=%{pginstdir}/bin/pg_config
export CUDA_PATH=%{__cuda_path}

%{__rm} -rf %{buildroot}
%{__make} -C src DESTDIR=%{buildroot} %{with_llvm_arg} install
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
* Sun Aug 30 2026 Devrim Gunduz <devrim@gunduz.org> - 6.1-3PGDG
- Make %%llvm actually control the build, not just packaging: pass
  with_llvm=no to make when %%llvm is 0, otherwise setting %%llvm 0 only
  dropped the llvm BuildRequires/subpackage/files while the build still
  invoked clang regardless, per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/51
- Note: the arrow-tools sub-build (arrow2csv/pg2arrow) is untouched by
  this, since those are standalone CLI tools, not PGXS-based PG extensions.

* Tue Jan 20 2026 Devrim Gündüz <devrim@gunduz.org> - 6.1-2PGDG
- Depend on Apache Arrow's packages. Please refer to
  https://yum.postgresql.org/extensions/pg_strom/ for details.

* Mon Nov 17 2025 Devrim Gündüz <devrim@gunduz.org> - 6.1-1PGDG
- Update to 6.1 per changes described at:
  https://heterodb.github.io/pg-strom/release_v6.1/

* Wed Oct 01 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com> - 6.0-2PGDG
- Bump release number (missed in previous commit)

* Tue Sep 30 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com>
- Change => to >= in Requires and BuildRequires

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
