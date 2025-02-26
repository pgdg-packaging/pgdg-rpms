%global sname postgresql-numeral

%{!?llvm:%global llvm 1}

Summary:	Numeric data types for PostgreSQL that use numerals
Name:		%{sname}_%{pgmajorversion}
Version:	1.3
Release:	3PGDG%{?dist}
License:	BSD
Source0:	https://github.com/df7cb/%{sname}/archive/refs/tags/v%{version}.tar.gz
URL:		https://github.com/df7cb//%{sname}
BuildRequires:	postgresql%{pgmajorversion}-devel bison flex
Requires:	postgresql%{pgmajorversion}-server

%description
postgresql-numeral provides numeric data types for PostgreSQL that use
numerals (words instead of digits) for input and output. Data types:
 - numeral: English numerals (one, two, three, four, ...), short scale (10⁹ = billion)
 - zahl: German numerals (eins, zwei, drei, vier, ...), long scale (10⁹ = Milliarde)
 - roman: Roman numerals (I, II, III, IV, ...)

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for postgresql-numeral
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
This package provides JIT support for postgresql-numeral
%endif

%prep
%setup -q -n %{sname}-%{version}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}
# Install README and howto file under PostgreSQL installation directory:
%{__install} -d %{buildroot}%{pginstdir}/doc/extension
%{__install} -m 644 README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md

%files
%defattr(644,root,root,755)
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%{pginstdir}/lib/numeral.so
%{pginstdir}/share/extension/numeral--*.sql
%{pginstdir}/share/extension/numeral.control

%if %llvm
%files llvmjit
    %{pginstdir}/lib/bitcode/numeral*.bc
    %{pginstdir}/lib/bitcode/numeral/*.bc
%endif

%changelog
* Wed Feb 26 2025 - Devrim Gündüz <devrim@gunduz.org> 1.3-3PGDG
- Add missing BRs

* Mon Jan 27 2025 - Devrim Gündüz <devrim@gunduz.org> 1.3-2PGDG
- Update LLVM dependencies

* Mon Sep 30 2024 - Devrim Gündüz <devrim@gunduz.org> 1.3-1PGDG
- Initial RPM packaging for PostgreSQL YUM Repository
