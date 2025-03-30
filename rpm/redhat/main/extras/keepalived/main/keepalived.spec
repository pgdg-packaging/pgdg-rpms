%bcond_without	snmp
%bcond_without	vrrp
%bcond_without	sha1
%bcond_without	json
%bcond_without	nftables
%bcond_with	profile
%bcond_with	debug

%global _hardened_build 1

Name:		keepalived
Summary:	High Availability monitor built upon LVS, VRRP and service pollers
Version:	2.3.3
Release:	1PGDG%{?dist}
License:	GPLv2+
URL:		https://www.keepalived.org/
Source0:	https://www.keepalived.org/software/keepalived-%{version}.tar.gz
Source1:	keepalived.service

Requires(post):		systemd
Requires(preun):	systemd
Requires(postun):	systemd

%if %{with snmp}
BuildRequires:	net-snmp-devel
%endif
%if %{with nftables}
BuildRequires:	libmnl-devel
BuildRequires:	libnftnl-devel
%else
BuildRequires:	ipset-devel
BuildRequires:	iptables-devel
%endif
BuildRequires:	gcc
BuildRequires:	systemd-devel
BuildRequires:	openssl-devel
BuildRequires:	libnl3-devel
BuildRequires:	libnfnetlink-devel
BuildRequires:	file-devel
BuildRequires:	make

%description
Keepalived provides simple and robust facilities for load balancing
and high availability to Linux system and Linux based infrastructures.
The load balancing framework relies on well-known and widely used
Linux Virtual Server (IPVS) kernel module providing Layer4 load
balancing. Keepalived implements a set of checkers to dynamically and
adaptively maintain and manage load-balanced server pool according
their health. High availability is achieved by VRRP protocol. VRRP is
a fundamental brick for router failover. In addition, keepalived
implements a set of hooks to the VRRP finite state machine providing
low-level and high-speed protocol interactions. Keepalived frameworks
can be used independently or all together to provide resilient
infrastructures.

%prep
%autosetup -p1

# Prevent re-running autotools.
touch aclocal.m4 Makefile.in lib/config.h.in configure

%build
%configure \
    %{?with_debug:--enable-debug} \
    %{?with_profile:--enable-profile} \
    %{!?with_vrrp:--disable-vrrp} \
    %{?with_snmp:--enable-snmp --enable-snmp-rfc} \
    %{?with_nftables:--enable-nftables --disable-iptables} \
    %{?with_json:--enable-json} \
    %{?with_sha1:--enable-sha1} \
    --with-init=systemd
%{__make} %{?_smp_mflags} STRIP=/bin/true

%install
%{__rm} -rf %{buildroot}
%{__make} install DESTDIR=%{buildroot}
%{__rm} -rf %{buildroot}%{_initrddir}/
%{__rm} -rf %{buildroot}%{_sysconfdir}/keepalived/samples/
%{__mv} %{buildroot}%{_sysconfdir}/keepalived/keepalived.conf.sample \
   %{buildroot}%{_sysconfdir}/keepalived/keepalived.conf
%{__install} -p -D -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/keepalived.service
%{__mkdir} -p %{buildroot}%{_libexecdir}/keepalived

# Remove duplicate README on SLES:
%if 0%{?suse_version} >= 1315
%{__rm} -f %{buildroot}%{_datadir}/doc/%{name}/README
%endif

%post
%systemd_post keepalived.service

%preun
%systemd_preun keepalived.service

%postun
%systemd_postun_with_restart keepalived.service

%files
%attr(0755,root,root) %{_sbindir}/keepalived
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/sysconfig/keepalived
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/keepalived/keepalived.conf
%doc AUTHOR ChangeLog CONTRIBUTORS COPYING README TODO
%doc doc/keepalived.conf.SYNOPSIS doc/samples/keepalived.conf.*
%dir %{_sysconfdir}/keepalived/
%dir %{_libexecdir}/keepalived/
%if %{with snmp}
%{_datadir}/snmp/mibs/KEEPALIVED-MIB.txt
%{_datadir}/snmp/mibs/VRRP-MIB.txt
%{_datadir}/snmp/mibs/VRRPv3-MIB.txt
%endif
%{_bindir}/genhash
%{_unitdir}/keepalived.service
%{_mandir}/man1/genhash.1*
%{_mandir}/man5/keepalived.conf.5*
%{_mandir}/man8/keepalived.8*

%changelog
* Sun Mar 30 2025 Devrim Gündüz <devrim@gunduz.org> - 2.3.3-1PGDG
- Update to 2.3.3 per changes described at:
  https://www.keepalived.org/release-notes/Release-2.3.3.html

* Mon Nov 4 2024 Devrim Gündüz <devrim@gunduz.org> - 2.3.2-1PGDG
- Update to 2.3.2 per changes described at:
  https://www.keepalived.org/release-notes/Release-2.3.2.html

* Mon May 27 2024 Devrim Gündüz <devrim@gunduz.org> - 2.3.1-1PGDG
- Update to 2.3.1 per changes described at:
  https://www.keepalived.org/release-notes/Release-2.3.1.html
  https://www.keepalived.org/release-notes/Release-2.3.0.html

* Wed Feb 21 2024 Devrim Gündüz <devrim@gunduz.org> - 2.2.8-2PGDG
- Remove redundant BR.

* Thu Jun 15 2023 Devrim Gündüz <devrim@gunduz.org> - 2.2.8-1
- Initial packaging for the PostgreSQL RPM repository to support
  Patroni installations. Spec file taken from Fedora rawhide.
