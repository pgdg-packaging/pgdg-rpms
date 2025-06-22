Summary:	Automatic reindexing of PostgreSQL indexes (bloat cleanup)
Name:		pg_auto_reindexer
Version:	1.5
Release:	1PGDG%{dist}
License:	MIT
Source0:	https://github.com/vitabaks/%{name}/archive/refs/tags/v%{version}.tar.gz
URL:		https://github.com/vitabaks/%{name}
BuildArch:	noarch

%description
pg_auto_reindexer automatically detects and reindexes bloated B-tree indexes
with minimal locking. It uses REINDEX CONCURRENTLY.

%prep
%setup -q -n %{name}-%{version}

%build
echo "no build step needed"

%install
%{__mkdir} -p %{buildroot}%{_bindir}
%{__install} -m 755 %{name} %{buildroot}%{_bindir}

%files
%defattr(-,root,root,-)
%doc README.md
%license LICENSE
%{_bindir}/%{name}

%changelog
* Sun Jun 22 2025 Devrim Gunduz <devrim@gunduz.org> - 1.5-1PGDG
- Initial RPM packaging for the PostgreSQL RPM Repository.
