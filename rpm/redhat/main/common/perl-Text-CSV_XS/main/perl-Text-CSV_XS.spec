%{!?runselftest:%global runselftest 0}

Name:		perl-Text-CSV_XS
Version:	1.65
Release:	42PGDG%{?dist}
Summary:	Comma-separated values manipulation routines
License:	GPL-1.0-or-later OR Artistic-1.0-Perl
URL:		https://metacpan.org/release/Text-CSV_XS
Source0:	https://cpan.metacpan.org/authors/id/H/HM/HMBRAND/Text-CSV_XS-%{version}.tgz

BuildRequires:	coreutils
BuildRequires:	findutils
BuildRequires:	gcc
BuildRequires:	make
BuildRequires:	perl-devel
BuildRequires:	perl-generators
BuildRequires:	perl-interpreter
BuildRequires:	perl(Carp)
BuildRequires:	perl(Encode)
BuildRequires:	perl(Exporter)
BuildRequires:	perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:	perl(IO::Handle)
BuildRequires:	perl(strict)
BuildRequires:	perl(vars)
BuildRequires:	perl(warnings)
BuildRequires:	perl(XSLoader)
%if %runselftest
BuildRequires:	perl(base)
BuildRequires:	perl(charnames)
BuildRequires:	perl(Config)
BuildRequires:	perl(Test::More)
BuildRequires:	perl(Tie::Scalar)
%endif

# Specific version >= 3.22 for Encode is recommended but not required
Requires:	perl(Encode)
# IO::Handle is loaded by XS code
Requires:	perl(IO::Handle)

# Text::CSV_XS calls UNIVERSAL::isa as the function built into perl, so the
# UNIVERSAL::isa CPAN module (EPEL only on RHEL) is not needed.

%{?perl_default_filter}

%description
Text::CSV provides facilities for the composition and decomposition of
comma-separated values.  An instance of the Text::CSV class can combine
fields into a CSV string and parse a CSV string into fields.

%prep
%setup -q -n Text-CSV_XS-%{version}

# These are examples, not scripts to run:
chmod -c a-x examples/*

%build
%{__perl} Makefile.PL \
	INSTALLDIRS=vendor \
	OPTIMIZE="%{optflags}" \
	NO_PACKLIST=true \
	NO_PERLLOCAL=true
%{make_build}

%install
%{make_install}
find %{buildroot} -type f -name '*.bs' -empty -delete
%{_fixperms} -c %{buildroot}

%check
%if %runselftest
%{make_build} test
%endif

%files
%doc ChangeLog CONTRIBUTING.md examples/ LOVE_LETTER.md README SECURITY.md
%{perl_vendorarch}/Text/
%{perl_vendorarch}/auto/Text/
%{_mandir}/man3/Text::CSV_XS.3*

%changelog
* Wed Oct 28 2026 Devrim Gunduz <devrim@gunduz.org> - 1.65-42PGDG
- Initial packaging for the PostgreSQL RPM repository, for pgbadger on RHEL
  8, 9 and 10, without EPEL. Based on the Fedora spec file. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/422
