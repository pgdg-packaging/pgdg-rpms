Summary:	PostgreSQL Database Security Assessment Tool
Name:		pgdsat
Version:	1.1
Release:	1PGDG%{?dist}
License:	GPLv3
URL:		https://github.com/HexaCluster/%{name}/
Source0:	https://github.com/HexaCluster/%{name}/archive/refs/tags/v%{version}.tar.gz
BuildRequires:	perl(ExtUtils::MakeMaker) make
%if 0%{?fedora} >= 40 || 0%{?rhel} >= 8
BuildRequires:	perl-macros
%endif
BuildArch:	noarch

%description
PGDSAT is a security assessment tool that checks around 70 PostgreSQL security
controls of your PostgreSQL clusters including all recommendations from the
CIS compliance benchmark but not only.

This tool is a single command that must be run on the PostgreSQL server to
collect all necessaries system and PostgreSQL information to compute a security
assessment report. A report consist in a summary of all tests status and a
second part with all detailed information.

%prep
%setup -q
%{__perl} Makefile.PL

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor

%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__make} pure_install PERL_INSTALL_ROOT=%{buildroot}

find %{buildroot} -type f -name .packlist -exec rm -f {} +
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null \;

%files
%defattr(-,root,root,-)
%attr(755,root,root) %{_bindir}/%{name}
%{_mandir}/man1/%{name}*
%{perl_vendorlib}/PGDSAT.pm
%{perl_vendorlib}/PGDSAT/*.pm

%changelog
* Mon Oct 20 2025 - Devrim Gündüz <devrim@gunduz.org> 1.1-1PGDG
- Initial RPM packaging for the PostgreSQL RPM Repository
