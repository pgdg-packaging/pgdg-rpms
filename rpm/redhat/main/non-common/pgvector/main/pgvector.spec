%global pname vector
%global sname pgvector

%{!?llvm:%global llvm 1}

Name:		%{sname}_%{pgmajorversion}
Version:	0.8.1
Release:	3PGDG%{?dist}
Summary:	Open-source vector similarity search for Postgres
License:	PostgreSQL
URL:		https://github.com/%{sname}/%{sname}/
Source0:	https://github.com/%{sname}/%{sname}/archive/refs/tags/v%{version}.tar.gz

# To be removed when upstream releases a version with this patch:
# https://github.com/pgvector/pgvector/pull/311
Patch0:		pgvector-0.6.2-fixillegalinstructionrror.patch

BuildRequires:	postgresql%{pgmajorversion}-devel
Requires:	postgresql%{pgmajorversion}-server

%description
Open-source vector similarity search for Postgres.

Store your vectors with the rest of your data. Supports:

* exact and approximate nearest neighbor search
* single-precision, half-precision, binary, and sparse vectors
* L2 distance, inner product, cosine distance, L1 distance, Hamming distance,
  and Jaccard distance
* any language with a Postgres client

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for pgvector
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
This package provides JIT support for pgvector
%endif

%prep
%setup -q -n %{sname}-%{version}
%patch -P 0 -p0

%build
USE_PGXS=1 PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}

#Remove header file, we don't need it right now:
%{__rm} %{buildroot}%{pginstdir}/include/server/extension/%{pname}/%{pname}.h

%files
%doc README.md
%license LICENSE
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension//%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%dir %{pginstdir}/include/server/extension/vector/
%{pginstdir}/include/server/extension/vector/*.h

%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/%{pname}*.bc
   %{pginstdir}/lib/bitcode/%{pname}/src/*.bc
%endif

%changelog
* Wed Oct 8 2025 Devrim Gündüz <devrim@gunduz.org> - 0.8.1-3PGDG
- Add SLES 16 support

* Wed Oct 01 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com> - 0.8.1-2PGDG
- Bump release number (missed in previous commit)

* Tue Sep 30 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com>
- Change => to >= in Requires and BuildRequires

* Fri Sep 5 2025 Devrim Gündüz <devrim@gunduz.org> - 0.8.1-1PGDG
- Update to 0.8.1

* Sun Jan 19 2025 Devrim Gündüz <devrim@gunduz.org> - 0.8.0-2PGDG
- Update package description

* Fri Nov 1 2024 Devrim Gündüz <devrim@gunduz.org> - 0.8.0-1PGDG
- Update to 0.8.0

* Tue Aug 6 2024 Devrim Gündüz <devrim@gunduz.org> - 0.7.4-1PGDG
- Update to 0.7.4

* Mon Jul 29 2024 Devrim Gündüz <devrim@gunduz.org> - 0.7.3-2PGDG
- Update LLVM dependencies

* Mon Jul 22 2024 Devrim Gündüz <devrim@gunduz.org> - 0.7.3-1PGDG
- Update to 0.7.3
- Remove RHEL 7 support

* Sat Jun 15 2024 Devrim Gündüz <devrim@gunduz.org> - 0.7.2-1PGDG
- Update to 0.7.2

* Tue Jun 4 2024 Devrim Gündüz <devrim@gunduz.org> - 0.7.1-1PGDG
- Update to 0.7.1

* Thu May 2 2024 Devrim Gündüz <devrim@gunduz.org> - 0.7.0-2PGDG
- Add a patch from upstream to fix extension instsallation on RHEL 8.
  https://github.com/pgvector/pgvector/issues/538

* Tue Apr 30 2024 Devrim Gündüz <devrim@gunduz.org> - 0.7.0-1PGDG
- Update to 0.7.0

* Wed Apr 3 2024 Devrim Gündüz <devrim@gunduz.org> - 0.6.2-2PGDG
  Add a patch to solve "illegal instruction error". This patch will be removed
  in 0.7.0 per: https://github.com/pgvector/pgvector/pull/311

* Wed Mar 20 2024 Devrim Gündüz <devrim@gunduz.org> - 0.6.2-1PGDG
- Update to 0.6.2

* Mon Mar 4 2024 Devrim Gündüz <devrim@gunduz.org> - 0.6.1-1PGDG
- Update to 0.6.1

* Mon Jan 29 2024 Devrim Gündüz <devrim@gunduz.org> - 0.6.0-1PGDG
- Update to 0.6.0

* Wed Oct 11 2023 Devrim Gündüz <devrim@gunduz.org> - 0.5.1-1PGDG
- Update to 0.5.1

* Thu Aug 31 2023 Devrim Gündüz <devrim@gunduz.org> - 0.5.0-1PGDG
- Update to 0.5.0
- Add PGDG branding

* Tue Jun 13 2023 Devrim Gündüz <devrim@gunduz.org> - 0.4.4-1
- Update to 0.4.4

* Sat Jun 03 2023 Devrim Gunduz <devrim@gunduz.org> - 0.4.2-1.1
- Rebuild against LLVM 15 on SLES 15

* Tue May 23 2023 Devrim Gündüz <devrim@gunduz.org> - 0.4.2-1
- Update to 0.4.2

* Thu Mar 30 2023 Devrim Gündüz <devrim@gunduz.org> - 0.4.1-1
- Initial packaging for PostgreSQL YUM repository.

