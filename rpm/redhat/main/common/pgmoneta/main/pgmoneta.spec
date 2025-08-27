Name:		pgmoneta
Version:	0.19.0
Release:	1PGDG%{dist}
Summary:	Backup / restore for PostgreSQL
License:	BSD
URL:		https://github.com/%{name}/%{name}
Source0:	https://github.com/%{name}/%{name}/archive/%{version}.tar.gz
Source1:	%{name}.service
Source2:	%{name}-tmpfiles.d

Patch0:		%{name}-conf-rpm.patch
BuildRequires:	gcc cmake make python3-docutils zlib-devel
BuildRequires:	libzstd-devel lz4-devel bzip2-devel
BuildRequires:	libev-devel openssl-devel systemd-devel
BuildRequires:	libssh-devel libarchive-devel cjson-devel libatomic
Requires:	libev openssl systemd zlib libzstd lz4 bzip2 libssh
Requires:	libarchive cjson


# Systemd stuff
BuildRequires:		systemd, systemd-devel
# We require this to be present for %%{_prefix}/lib/tmpfiles.d
Requires:		systemd
%if 0%{?suse_version}
%if 0%{?suse_version} >= 1499
Requires(post):		systemd-sysvinit
%endif
%else
Requires(post):		systemd-sysv
Requires(post):		systemd
Requires(preun):	systemd
Requires(postun):	systemd
%endif

Obsoletes:	%{name}_13 < 0.2.0-2

%description
pgmoneta is a backup / restore solution for PostgreSQL.

%prep
%setup -q -n %{name}-%{version}
%patch -P 0 -p0

%build

%{__mkdir} build
cd build
cmake -DCMAKE_BUILD_TYPE=Release .. -DCMAKE_INSTALL_PREFIX=/usr
%{__make}

%install
cd build
%{__make} install DESTDIR=%{buildroot}

# Install some files manually
%{__mkdir} -p %{buildroot}%{_docdir}/%{name}/shell_comp
%{__mkdir} -p %{buildroot}%{_docdir}/%{name}/tutorial
%{__install} -m 644 %{_builddir}/%{name}-%{version}/contrib/shell_comp/pgmoneta_comp.* %{buildroot}%{_docdir}/%{name}/shell_comp/
%{__install} -m 644 %{_builddir}/%{name}-%{version}/doc/tutorial/0*.md %{buildroot}%{_docdir}/%{name}/tutorial/

# Install config file
%{__mkdir} -p %{buildroot}%{_sysconfdir}/%{name}
%{__mv} %{buildroot}/%{_docdir}/%{name}/etc/%{name}.conf %{buildroot}%{_sysconfdir}/%{name}

# Install unit file
%{__install} -d %{buildroot}%{_unitdir}
%{__install} -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service

# ... and make a tmpfiles script to recreate it at reboot.
%{__mkdir} -p %{buildroot}/%{_tmpfilesdir}
%{__install} -m 0644 %{SOURCE2} %{buildroot}/%{_tmpfilesdir}/%{name}.conf

%post
%{__chown} -R postgres:postgres %{_sysconfdir}/%{name}
%{__mkdir} -p /var/log/%{name}
%{__chown} -R postgres:postgres /var/log/%{name}
if [ $1 -eq 1 ] ; then
   /bin/systemctl daemon-reload >/dev/null 2>&1 || :
   %if 0%{?suse_version}
    %if 0%{?suse_version} >= 1499
     %service_add_pre %{same}.service
    %endif
   %else
    %systemd_post %{name}.service
    %endif
fi

%preun
if [ $1 -eq 0 ] ; then
	# Package removal, not upgrade
	/bin/systemctl --no-reload disable %{name}.service >/dev/null 2>&1 || :
	/bin/systemctl stop %{name}.service >/dev/null 2>&1 || :
fi

%postun
if [ $1 -ge 1 ] ; then
	# Package upgrade, not uninstall
	/bin/systemctl try-restart %{name}.service >/dev/null 2>&1 || :
fi

%files
%license LICENSE
%{_bindir}/%{name}
%{_bindir}/%{name}-admin
%{_bindir}/%{name}-cli
%{_bindir}/%{name}-walinfo
%config %{_sysconfdir}/%{name}/%{name}.conf
%{_libdir}/libpgmoneta.so*
%dir %{_docdir}/%{name}
%{_docdir}/%{name}/*
%{_mandir}/man1/%{name}*
%{_mandir}/man5/%{name}*
%{_tmpfilesdir}/%{name}.conf
%{_unitdir}/%{name}.service

%changelog
* Wed Aug 27 2025 Devrim Gündüz <devrim@gunduz.org> 0.19.0-1PGDG
- Update to 0.19.0 per changes described at:
  https://github.com/pgmoneta/pgmoneta/releases/tag/0.19.0

* Fri Jul 11 2025 Devrim Gündüz <devrim@gunduz.org> 0.18.0-1PGDG
- Update to 0.18.0 per changes described at:
  https://github.com/pgmoneta/pgmoneta/releases/tag/0.18.0

* Wed Jun 18 2025 Devrim Gündüz <devrim@gunduz.org> 0.17.2-1PGDG
- Update to 0.17.2 per changes described at:
  https://github.com/pgmoneta/pgmoneta/releases/tag/0.17.2
  https://github.com/pgmoneta/pgmoneta/releases/tag/0.17.1

* Fri May 23 2025 Devrim Gündüz <devrim@gunduz.org> 0.17.0-1PGDG
- Update to 0.17.0 per changes described at:
  https://github.com/pgmoneta/pgmoneta/releases/tag/0.17.0

* Mon May 5 2025 Devrim Gündüz <devrim@gunduz.org> 0.16.1-1PGDG
- Update to 0.16.1 per changes described at:
  https://github.com/pgmoneta/pgmoneta/releases/tag/0.16.1

* Wed Apr 23 2025 Devrim Gündüz <devrim@gunduz.org> 0.16.0-1PGDG
- Update to 0.16.0 per changes described at:
  https://github.com/pgmoneta/pgmoneta/releases/tag/0.16.0

* Wed Feb 19 2025 Devrim Gündüz <devrim@gunduz.org> 0.15.2-1PGDG
- Update to 0.15.2 per changes described at:
  https://github.com/pgmoneta/pgmoneta/releases/tag/0.15.2
- Remove patch1

* Sun Jan 5 2025 Devrim Gündüz <devrim@gunduz.org> 0.15.1-1PGDG
- Update to 0.15.1 per changes described at:
  https://github.com/pgmoneta/pgmoneta/releases/tag/0.15.1
- Add a temp patch per https://redmine.postgresql.org/issues/8084#note-2

* Thu Dec 19 2024 Devrim Gündüz <devrim@gunduz.org> 0.15.0-1PGDG
- Update to 0.15.0 per changes described at:
  https://github.com/pgmoneta/pgmoneta/releases/tag/0.15.0
- Add a temp patch, per https://redmine.postgresql.org/issues/8081

* Wed Sep 25 2024 Devrim Gündüz <devrim@gunduz.org> 0.14.1-1PGDG
- Update to 0.14.1 per changes described at:
  https://github.com/pgmoneta/pgmoneta/releases/tag/0.14.1

* Tue Sep 17 2024 Devrim Gündüz <devrim@gunduz.org> 0.14.0-1PGDG
- Update to 0.14.0 per changes described at:
  https://github.com/pgmoneta/pgmoneta/releases/tag/0.14.0

* Mon Aug 5 2024 Devrim Gündüz <devrim@gunduz.org> 0.13.0-1PGDG
- Update to 0.13.0 per changes described at:
  https://github.com/pgmoneta/pgmoneta/releases/tag/0.13.0

* Mon Jun 17 2024 Devrim Gündüz <devrim@gunduz.org> 0.12.0-1PGDG
- Update to 0.12.0 per changes described at:
  https://pgmoneta.github.io/_posts/2024-06-05-pgmoneta-0.12.0.html

* Wed May 1 2024 Devrim Gündüz <devrim@gunduz.org> 0.11.1-1PGDG
- Update to 0.11.1 per changes described at:
  https://pgmoneta.github.io/_posts/2024-04-30-pgmoneta-0.11.1.html

* Sat Apr 27 2024 Devrim Gündüz <devrim@gunduz.org> 0.11.0-1PGDG
- Update to 0.11.0 per changes described at:
  https://pgmoneta.github.io//release/announcement/2024/04/23/pgmoneta-0.11.0.html

* Fri Apr 5 2024 Devrim Gündüz <devrim@gunduz.org> 0.10.1-1PGDG
- Update to 0.10.1 per changes described at:
  https://pgmoneta.github.io//release/announcement/2024/04/05/pgmoneta-0.10.1.html

* Mon Apr 1 2024 Devrim Gündüz <devrim@gunduz.org> 0.10.0-1PGDG
- Update to 0.10.0 per changes described at:
  https://pgmoneta.github.io//release/announcement/2024/03/28/pgmoneta-0.10.0.html

* Thu Feb 15 2024 Devrim Gündüz <devrim@gunduz.org> 0.9.0-1PGDG
- Update to 0.9.0 per changes described at:
  https://pgmoneta.github.io/release/announcement/2024/02/14/pgmoneta-0.9.0.html

* Tue Jan 23 2024 Devrim Gündüz <devrim@gunduz.org> 0.8.0-1PGDG
- Update to 0.8.0 per changes described at:
  https://pgmoneta.github.io/release/announcement/2024/01/22/pgmoneta-0.8.0.html

* Thu Dec 28 2023 Devrim Gündüz <devrim@gunduz.org> 0.7.3-1PGDG
- Update to 0.7.3 per changes described at:
  https://pgmoneta.github.io/release/announcement/2023/12/28/pgmoneta-0.7.3.html

* Thu Dec 21 2023 Devrim Gündüz <devrim@gunduz.org> 0.7.2-1PGDG
- Update to 0.7.2 per changes described at:
  https://pgmoneta.github.io/release/announcement/2023/12/13/pgmoneta-0.7.2.html

* Sun Oct 22 2023 Devrim Gündüz <devrim@gunduz.org> 0.7.1-1PGDG
- Update to 0.7.1 per changes described at:
  https://pgmoneta.github.io/release/announcement/2023/10/22/pgmoneta-0.7.1.html

* Fri Oct 6 2023 Devrim Gündüz <devrim@gunduz.org> 0.7.0-1PGDG
- Update to 0.7.0 per changes described at:
  https://pgmoneta.github.io/release/announcement/2023/09/28/pgmoneta-0.7.0.html
- Add PGDG branding

* Mon Apr 24 2023 Devrim Gunduz <devrim@gunduz.org> - 0.6.1-1.1
- Modernise %%patch usage, which has been deprecated in Fedora 38

* Thu Jan 12 2023 Devrim Gündüz <devrim@gunduz.org> 0.6.1-1
- Update to 0.6.1

* Fri Sep 23 2022 Devrim Gündüz <devrim@gunduz.org> 0.6.0-1
- Update to 0.6.0

* Thu Aug 11 2022 Devrim Gündüz <devrim@gunduz.org> 0.5.7-1
- Update to 0.5.7

* Fri May 27 2022 Devrim Gündüz <devrim@gunduz.org> 0.5.6-1
- Update to 0.5.6

* Mon Jan 10 2022 Devrim Gündüz <devrim@gunduz.org> 0.5.5-1
- Update to 0.5.5

* Thu Nov 25 2021 Devrim Gündüz <devrim@gunduz.org> 0.5.4-1
- Update to 0.5.4

* Fri Oct 22 2021 Devrim Gündüz <devrim@gunduz.org> 0.5.3-1
- Update to 0.5.3

* Sat Oct 16 2021 Devrim Gündüz <devrim@gunduz.org> 0.5.2-1
- Update to 0.5.2

* Thu Sep 23 2021 Devrim Gündüz <devrim@gunduz.org> 0.5.1-1
- Update to 0.5.1

* Wed Sep 1 2021 Devrim Gündüz <devrim@gunduz.org> 0.5.0-2
- Add systemd support (unit file and tmpfiles.d support)
- Create log directory

* Thu Aug 26 2021 Devrim Gündüz <devrim@gunduz.org> 0.5.0-1
- Update to 0.5.0

* Thu Aug 12 2021 Devrim Gündüz <devrim@gunduz.org> 0.4.0-1
- Update to 0.4.0

* Tue Jul 20 2021 Devrim Gündüz <devrim@gunduz.org> 0.3.1-1
- Update to 0.3.1

* Sun Jul 4 2021 Devrim Gündüz <devrim@gunduz.org> 0.3.0-1
- Update to 0.3.0

* Thu Jun 17 2021 Devrim Gündüz <devrim@gunduz.org> 0.2.0-2
- Remove PostgreSQL version number from the package. This
  is a common one.

* Mon Jun 14 2021 Devrim Gündüz <devrim@gunduz.org> 0.2.0-1
- Update to 0.2.0

* Fri May 28 2021 Devrim Gündüz <devrim@gunduz.org> 0.1.0-1
- Initial packaging for PostgreSQL RPM repository. Took spec
  file from upstream.
