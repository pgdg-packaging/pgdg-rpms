%define haproxy_user	haproxy
%define haproxy_group	%{haproxy_user}
%define haproxy_homedir	%{_localstatedir}/lib/haproxy
%define haproxy_confdir	%{_sysconfdir}/haproxy
%define haproxy_datadir	%{_datadir}/haproxy

%global _hardened_build 1

Name:		haproxy
Version:	3.2.4
Release:	1PGDG%{?dist}
Summary:	HAProxy reverse proxy for high availability environments

License:	GPLv2+

URL:		https://www.haproxy.org/
Source0:	https://www.haproxy.org/download/3.2/src/%{name}-%{version}.tar.gz
Source1:	%{name}.service
Source2:	%{name}.cfg
Source3:	%{name}.logrotate
Source4:	%{name}.sysconfig
Source5:	halog.1

BuildRequires:	gcc lua-devel pcre2-devel make
BuildRequires:	openssl-devel systemd-devel systemd

%if 0%{?fedora} >= 40 || 0%{?rhel} >= 8
Requires(pre):	shadow-utils
%else
Requires(pre):	shadow
%endif

%{?systemd_requires}

%description
HAProxy is a TCP/HTTP reverse proxy which is particularly suited for high
availability environments. Indeed, it can:
 - route HTTP requests depending on statically assigned cookies
 - spread load among several servers while assuring server persistence
   through the use of HTTP cookies
 - switch to backup servers in the event a main one fails
 - accept connections to special ports dedicated to service monitoring
 - stop accepting connections without breaking existing ones
 - add, modify, and delete HTTP headers in both directions
 - block requests matching particular patterns
 - report detailed status to authenticated users from a URI
   intercepted from the application

%prep
%setup -q

%build
regparm_opts=
%ifarch %ix86 x86_64
regparm_opts="USE_REGPARM=1"
%endif

%{__make} %{?_smp_mflags} CPU="generic" TARGET="linux-glibc" USE_OPENSSL=1 USE_PCRE2=1 USE_SLZ=1 USE_LUA=1 USE_CRYPT_H=1 USE_SYSTEMD=1 USE_LINUX_TPROXY=1 USE_GETADDRINFO=1 USE_PROMEX=1 DEFINE=-DMAX_SESS_STKCTR=12 ${regparm_opts} \
%if 0%{?fedora} >= 40 || 0%{?rhel} >= 8
	ADDLIB="%{build_ldflags}" \
%endif
	ADDINC="%{build_cflags}"

%{__make} admin/halog/halog \
%if 0%{?fedora} >= 40 || 0%{?rhel} >= 8
	ADDLIB="%{build_ldflags}" \
%endif
	ADDINC="%{build_cflags}"

pushd admin/iprange
%{__make} \
%if 0%{?fedora} >= 40 || 0%{?rhel} >= 8
	LDFLAGS="%{build_ldflags}" \
%endif
	OPTIMIZE="%{build_cflags}"
popd

%install
%{__make} install-bin DESTDIR=%{buildroot} PREFIX=%{_prefix} SBINDIR=%{_sbindir} TARGET="linux2628"
%{__make} install-man DESTDIR=%{buildroot} PREFIX=%{_prefix}

%{__install} -p -D -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service
%{__install} -p -D -m 0644 %{SOURCE2} %{buildroot}%{haproxy_confdir}/%{name}.cfg
%{__install} -p -D -m 0644 %{SOURCE3} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}
%{__install} -p -D -m 0644 %{SOURCE4} %{buildroot}%{_sysconfdir}/sysconfig/%{name}
%{__install} -p -D -m 0644 %{SOURCE5} %{buildroot}%{_mandir}/man1/halog.1
%{__install} -d -m 0755 %{buildroot}%{haproxy_homedir}
%{__install} -d -m 0755 %{buildroot}%{haproxy_datadir}
%{__install} -d -m 0755 %{buildroot}%{_bindir}
%{__install} -p -m 0755 ./admin/halog/halog %{buildroot}%{_bindir}/halog
%{__install} -p -m 0755 ./admin/iprange/iprange %{buildroot}%{_bindir}/iprange
%{__install} -p -m 0755 ./admin/iprange/ip6range %{buildroot}%{_bindir}/ip6range

for httpfile in $(find ./examples/errorfiles/ -type f)
do
    %{__install} -p -m 0644 $httpfile %{buildroot}%{haproxy_datadir}
done

%{__rm} -rf ./examples/errorfiles/

find ./examples/* -type f ! -name "*.cfg" -exec %{__rm} -f "{}" \;

for textfile in $(find ./ -type f -name '*.txt')
do
    %{__mv} $textfile $textfile.old
    iconv --from-code ISO8859-1 --to-code UTF-8 --output $textfile $textfile.old
    %{__rm} -f $textfile.old
done

%pre
getent group %{haproxy_group} >/dev/null || \
    groupadd -r %{haproxy_group}
getent passwd %{haproxy_user} >/dev/null || \
    useradd -r -g %{haproxy_user} -d %{haproxy_homedir} \
    -s /sbin/nologin -c "haproxy" %{haproxy_user}
exit 0

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%files
%doc doc/* examples/*
%doc CHANGELOG VERSION
%license LICENSE
%dir %{haproxy_homedir}
%dir %{haproxy_confdir}
%dir %{haproxy_datadir}
%{haproxy_datadir}/*
%config(noreplace) %{haproxy_confdir}/%{name}.cfg
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%{_unitdir}/%{name}.service
%{_sbindir}/%{name}
%{_bindir}/halog
%{_bindir}/iprange
%{_bindir}/ip6range
%{_mandir}/man1/*

%changelog
* Mon Aug 18 2025 Devrim Gündüz <devrim@gunduz.org> 3.2.4-1PGDG
- Update to 3.2.4 per changes described at:
  https://www.mail-archive.com/haproxy@formilux.org/msg46051.html

* Wed Jul 23 2025 Devrim Gündüz <devrim@gunduz.org> 3.2.3-1PGDG
- Update to 3.2.3 per changes described at:
  https://www.mail-archive.com/haproxy@formilux.org/msg45983.html
  https://www.mail-archive.com/haproxy@formilux.org/msg45965.html

* Mon Jun 16 2025 Devrim Gündüz <devrim@gunduz.org> 3.2.1-1PGDG
- Update to 3.2.1 per changes described at:
  https://www.mail-archive.com/haproxy@formilux.org/msg45947.html

* Wed Jun 4 2025 Devrim Gündüz <devrim@gunduz.org> 3.2.0-1PGDG
- Update to 3.2.0 per changes described at:
  https://www.mail-archive.com/haproxy@formilux.org/msg45917.html

* Wed Apr 23 2025 Devrim Gündüz <devrim@gunduz.org> 3.1.7-1PGDG
- Update to 3.1.7 per changes described at:
  https://www.mail-archive.com/haproxy@formilux.org/msg45795.html

* Mon Mar 24 2025 Devrim Gündüz <devrim@gunduz.org> 3.1.6-1PGDG
- Update to 3.1.6 per changes described at:
  https://www.mail-archive.com/haproxy@formilux.org/msg45683.html

* Thu Feb 20 2025 Devrim Gündüz <devrim@gunduz.org> 3.1.5-1PGDG
- Update to 3.1.5 per changes described at:
  https://www.mail-archive.com/haproxy@formilux.org/msg45610.html

* Wed Feb 19 2025 Devrim Gündüz <devrim@gunduz.org> 3.1.4-1PGDG
- Update to 3.1.4 per changes described at:
  https://www.mail-archive.com/haproxy@formilux.org/msg45606.html

* Tue Feb 4 2025 Devrim Gündüz <devrim@gunduz.org> 3.1.3-1PGDG
- Update to 3.1.3 per changes described at:
  https://www.mail-archive.com/haproxy@formilux.org/msg45567.html

* Fri Jan 24 2025 Devrim Gündüz <devrim@gunduz.org> 3.1.2-1PGDG
- Update to 3.1.2 per changes described at:
  https://www.mail-archive.com/haproxy@formilux.org/msg45549.html

* Mon Dec 16 2024 Devrim Gündüz <devrim@gunduz.org> 3.1.1-1PGDG
- Update to 3.1.1 per changes described at:
  https://www.mail-archive.com/haproxy@formilux.org/msg45482.html

* Fri Dec 6 2024 Devrim Gündüz <devrim@gunduz.org> 3.1.0-1PGDG
- Update to 3.1.0 per changes described at:
  https://www.mail-archive.com/haproxy@formilux.org/msg45435.html

* Sat Nov 9 2024 - Devrim Gündüz <devrim@gunduz.org> 3.0.6-1PGDG
- Update to 3.0.6 per changes described at:
  https://www.mail-archive.com/haproxy@formilux.org/msg45411.html

* Thu Sep 19 2024 - Devrim Gündüz <devrim@gunduz.org> 3.0.5-1PGDG
- Update to 3.0.5 per changes described at:
  https://www.mail-archive.com/haproxy@formilux.org/msg45314.html

* Wed Sep 4 2024 - Devrim Gündüz <devrim@gunduz.org> 3.0.4-1PGDG
- Update to 3.0.4 per changes described at:
  https://www.mail-archive.com/haproxy@formilux.org/msg45280.html

* Fri Jul 12 2024 - Devrim Gündüz <devrim@gunduz.org> 3.0.3-1PGDG
- Update to 3.0.3 per changes described at:
  https://www.mail-archive.com/haproxy@formilux.org/msg45103.html

* Fri Jun 14 2024 - Devrim Gündüz <devrim@gunduz.org> 3.0.2-1PGDG
- Update to 3.0.2 per changes described at:
  https://www.mail-archive.com/haproxy@formilux.org/msg45058.html

* Tue Jun 11 2024 - Devrim Gündüz <devrim@gunduz.org> 3.0.1-1PGDG
- Update to 3.0.1 per changes described at:
  https://www.mail-archive.com/haproxy@formilux.org/msg45045.html

* Mon Jun 10 2024 - Devrim Gündüz <devrim@gunduz.org> 3.0.0-1PGDG
- Update to 3.0.0 per changes described at:
  https://www.mail-archive.com/haproxy@formilux.org/msg44993.html

* Sun Apr 7 2024 - Devrim Gündüz <devrim@gunduz.org> 2.9.7-1PGDG
- Update to 2.9.7 per changes described at:
  https://www.mail-archive.com/haproxy@formilux.org/msg44788.html

* Wed Feb 21 2024 - Devrim Gündüz <devrim@gunduz.org> 2.9.5-2PGDG
- Fix builds on SLES-15

* Sat Feb 17 2024 - Devrim Gündüz <devrim@gunduz.org> 2.9.5-1PGDG
- Update to 2.9.5 per changes described at:
  https://www.mail-archive.com/haproxy@formilux.org/msg44603.html

* Thu Feb 1 2024 - Devrim Gündüz <devrim@gunduz.org> 2.9.4-1PGDG
- Update to 2.9.4 per changes described at:
  https://www.mail-archive.com/haproxy@formilux.org/msg44547.html

* Sat Jan 20 2024 - Devrim Gündüz <devrim@gunduz.org> 2.9.3-1PGDG
- Update to 2.9.3 per changes described at:
  https://www.mail-archive.com/haproxy@formilux.org/msg44501.html

* Mon Jan 15 2024 - Devrim Gündüz <devrim@gunduz.org> 2.9.2-1PGDG
- Update to 2.9.2 per changes described at:
  https://www.mail-archive.com/haproxy@formilux.org/msg44481.html

* Fri Dec 29 2023 - Devrim Gündüz <devrim@gunduz.org> 2.9.1-1PGDG
- Update to 2.9.1 per changes described at:
  https://www.mail-archive.com/haproxy@formilux.org/msg44428.html

* Fri Dec 8 2023 - Devrim Gündüz <devrim@gunduz.org> 2.9.0-1PGDG
- Update to 2.9.0 per changes described at:
  https://www.mail-archive.com/haproxy@formilux.org/msg44400.html

* Sun Nov 19 2023 - Devrim Gündüz <devrim@gunduz.org> 2.8.4-1PGDG
- Update to 2.8.4

* Fri Sep 8 2023 - Devrim Gündüz <devrim@gunduz.org> 2.8.3-1PGDG
- Update to 2.8.3

* Wed Aug 9 2023 - Devrim Gündüz <devrim@gunduz.org> 2.8.2-1PGDG
- Update to 2.8.2
- Add PGDG branding

* Mon Jul 3 2023 - Devrim Gündüz <devrim@gunduz.org> 2.8.1-1
- Update to 2.8.1

* Fri Jun 2 2023 - Devrim Gündüz <devrim@gunduz.org> 2.8.0-1
- Update to 2.8.0

* Thu May 4 2023 - Devrim Gündüz <devrim@gunduz.org> 2.7.8-1
- Update to 2.7.8

* Mon Apr 10 2023 - Devrim Gündüz <devrim@gunduz.org> 2.7.6-1
- Update to 2.7.6

* Tue Mar 21 2023 - Devrim Gündüz <devrim@gunduz.org> 2.7.5-1
- Update to 2.7.5

* Sun Mar 12 2023 - Devrim Gündüz <devrim@gunduz.org> 2.7.4-1
- Update to 2.7.4

* Wed Feb 15 2023 - Devrim Gündüz <devrim@gunduz.org> 2.7.3-1
- Update to 2.7.3

* Mon Jan 30 2023 - Devrim Gündüz <devrim@gunduz.org> 2.7.2-1
- Update to 2.7.2

* Tue Dec 20 2022 - Devrim Gündüz <devrim@gunduz.org> 2.7.1-1
- Update to 2.7.1

* Thu Dec 15 2022 - Devrim Gündüz <devrim@gunduz.org> 2.7.0-1
- Update to 2.7.0

* Thu Dec 15 2022 - Devrim Gündüz <devrim@gunduz.org> 2.6.7-1
- Update to 2.6.7

* Fri Sep 23 2022 - Devrim Gündüz <devrim@gunduz.org> 2.6.6-1
- Update to 2.6.6

* Fri Sep 9 2022 - Devrim Gündüz <devrim@gunduz.org> 2.6.5-1
- Update to 2.6.5

* Mon Aug 22 2022 - Devrim Gündüz <devrim@gunduz.org> 2.6.3-1
- Update to 2.6.3

* Wed Jul 27 2022 - Devrim Gündüz <devrim@gunduz.org> 2.6.2-1
- Update to 2.6.2

* Tue May 31 2022 - Devrim Gündüz <devrim@gunduz.org> 2.5.7-1
- Update to 2.5.7

* Wed May 11 2022 - Devrim Gündüz <devrim@gunduz.org> 2.5.6-1
- Update to 2.5.6

* Wed Apr 20 2022 - Devrim Gündüz <devrim@gunduz.org> 2.5.5-1
- Update to 2.5.5

* Mon Mar 14 2022 - Devrim Gündüz <devrim@gunduz.org> 2.5.4-1
- Initial RPM packaging for the PostgreSQL RPM Repository
