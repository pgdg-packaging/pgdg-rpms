%if 0%{?fedora} && 0%{?fedora} == 45
%global python3_pkgversion 3.15
%global pybasever 3.15
%endif
%if 0%{?fedora} && 0%{?fedora} <= 44
%global python3_pkgversion 3.14
%global pybasever 3.14
%endif
%if 0%{?rhel} && 0%{?rhel} <= 10
%global	python3_pkgversion 3.12
%global	pybasever 3.12
%endif
%if 0%{?amzn} == 2023
%global	__python3 %{_bindir}/python3.13
%global	python3_pkgversion 3.13
%global	pybasever 3.13
%endif
%if 0%{?suse_version} == 1500
%global	python3_pkgversion 311
%global	pybasever 3.11
%endif
%if 0%{?suse_version} == 1600
%global	python3_pkgversion 313
%global	pybasever 3.13
%endif
# pybasever is used for the pythonX.Ydist() Requires below, whose names are
# the same on every distro (package names are not: e.g. SUSE's
# python313-Pygments vs. python3-pygments elsewhere). It is set statically
# because the interpreter is not yet installed when mock first parses the spec.

%{?python_disable_dependency_generator}

Summary:	A PostgreSQL client that does auto-completion and syntax highlighting
Name:		pgcli
Version:	4.7.1
Release:	2PGDG%{?dist}
# The exceptions allow linking to OpenSSL and PostgreSQL's libpq
License:	LGPLv3+ with exceptions
Url:		https://github.com/dbcli/%{name}
Source0:	https://files.pythonhosted.org/packages/source/p/%{name}/%{name}-%{version}.tar.gz

%if 0%{?suse_version} >= 1500
BuildRequires:	python-rpm-macros
%else
BuildRequires:	pyproject-rpm-macros
%endif
BuildRequires:	python%{python3_pkgversion}-devel
BuildRequires:	python%{python3_pkgversion}-pip
BuildRequires:	python%{python3_pkgversion}-setuptools
BuildRequires:	python%{python3_pkgversion}-setuptools_scm
BuildRequires:	python%{python3_pkgversion}-wheel

Requires:	python3-%{name} = %{version}-%{release}
Requires:	python%{pybasever}dist(cli-helpers) >= 2.4.0
Requires:	python%{pybasever}dist(click) >= 4.1
Requires:	python%{pybasever}dist(configobj) >= 5.0.6
Requires:	python%{pybasever}dist(pgspecial) >= 2.0.0
Requires:	python%{pybasever}dist(prompt-toolkit) >= 2.0.6
Requires:	python%{pybasever}dist(psycopg) >= 3.0.14
Requires:	python%{pybasever}dist(pygments) >= 2.0
Requires:	python%{pybasever}dist(setproctitle) >= 1.1.9
Requires:	python%{pybasever}dist(sqlparse) >= 0.3.0
# Upstream asks for tzlocal >= 5.2, but pgcli only uses get_localzone_name(),
# which is available since 4.0. Leap 16 ships 4.3.
Requires:	python%{pybasever}dist(tzlocal)
BuildArch:	noarch

%description
This is a PostgreSQL client that does auto-completion and syntax highlighting.

%package -n python3-%{name}
Summary:	A PostgreSQL client that does auto-completion and syntax highlighting for Python 3

%description -n python3-%{name}
This is a build of pgcli the for the Python 3.

%package -n python3-%{name}-debug
Summary:	A PostgreSQL client that does auto-completion and syntax highlighting for Python 3 (debug build)
# Require base python 3 package, as we're sharing .py/.pyc files:
Requires:	python3-%{name} = %{version}-%{release}

%description -n python3-%{name}-debug
This is a build of the pgcli for the debug build of Python 3.

%prep
%setup -q
# Upstream declares license as a bare PEP 639 SPDX string, which the
# setuptools shipped on RHEL 9/10 and Leap 16 is too old to validate
# ("project.license must be valid exactly by one definition"). Rewrite
# it to the older PEP 621 {text = ...} form, which every setuptools in
# our build matrix accepts.
sed -i 's/^license = "BSD-3-Clause"$/license = {text = "BSD-3-Clause"}/' pyproject.toml

%build
%pyproject_wheel

%install
%pyproject_install
%files
%defattr(-,root,root)
%doc AUTHORS changelog.rst LICENSE.txt TODO
%{_bindir}/%{name}

%files -n python3-%{name}
%defattr(-,root,root)
%doc AUTHORS changelog.rst LICENSE.txt TODO
%dir %{python3_sitelib}/%{name}
%{python3_sitelib}/%{name}/*
%{python3_sitelib}/%{name}-%{version}.dist-info/

%files -n python3-%{name}-debug
%defattr(-,root,root)
%doc LICENSE.txt

%changelog
* Tue Sep 22 2026 Devrim Gündüz <devrim@gunduz.org> - 4.7.1-2PGDG
- Sync runtime Requires with upstream's pyproject.toml. Add the missing
  pgspecial, prompt-toolkit, psycopg3 and tzlocal dependencies, and drop
  jedi, humanize and wcwidth, which pgcli no longer uses. Fixes BUG #19562.
  Per report and patch from Pritt Balagopal.
- Use the same Python version mapping as pglast. pgcli 4.7 requires
  Python >= 3.10.
- Remove the RHEL 9 setup.py workaround. It was only needed for the old
  setuptools of RHEL 9's system python3.9.
- Express Requires as pythonX.Ydist() names, which are the same on all
  distros, and drop the unused test BuildRequires (there is no %%check).

* Sun Sep 20 2026 Devrim Gündüz <devrim@gunduz.org> - 4.7.1-1PGDG
- Update to 4.7.1 per changes described at:
  https://github.com/dbcli/pgcli/releases/tag/v4.7.1

* Sat Sep 19 2026 Devrim Gündüz <devrim@gunduz.org> - 4.7.0-1PGDG
- Update to 4.7.0 per changes described at:
  https://github.com/dbcli/pgcli/releases/tag/v4.7.0
- Add BR for setuptools_scm. Upstream derives the version through it, and
  without it the wheel is built as pgcli-0.0.0, so the %%files entry for
  pgcli-%%{version}.dist-info does not match.
- Drop the %%global python3_sitelib override, which used distutils
  (removed in Python 3.12); the macro is already provided by python3-devel
  and python-rpm-macros.
- Rewrite the bare PEP 639 SPDX license string in pyproject.toml to the
  older PEP 621 {text = ...} form in %%prep, because the setuptools on RHEL
  10 (and others) rejects it.
- Fix the RHEL 9 build and add the missing python3-wheel BR.

* Thu Sep 10 2026 Devrim Gündüz <devrim@gunduz.org> - 4.6.0-3PGDG
- Add missing BR

* Fri Aug 28 2026 Devrim Gündüz <devrim@gunduz.org> - 4.6.0-2PGDG
- Package the .dist-info directory itself instead of globbing only its
  contents (dist-info/*), matching correct RPM directory-packaging
  practice (this package explicitly disables the Python dependency
  generator via python_disable_dependency_generator and declares its
  Requires by hand, so this has no functional effect here). Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/226

* Thu Aug 27 2026 Devrim Gündüz <devrim@gunduz.org> - 4.6.0-1PGDG
- Update to 4.6.0

* Fri Jun 5 2026 Devrim Gündüz <devrim@gunduz.org> - 4.5.0-1PGDG
- Update to 4.5.0

* Wed Oct 01 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com> - 4.3.0-2PGDG
- Bump release number (missed in previous commit)

* Tue Sep 30 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com>
- Change => to >= in Requires and BuildRequires

* Sun Mar 23 2025 Devrim Gündüz <devrim@gunduz.org> - 4.3.0-1PGDG
- Update to 4.3.0

* Fri Aug 23 2024 Devrim Gündüz <devrim@gunduz.org> - 4.1.0-1PGDG
- Update to 4.1.0

* Mon Feb 19 2024 Devrim Gündüz <devrim@gunduz.org> - 4.0.1-1PGDG
- Update to 4.0.1
- Add PGDG branding

* Fri Sep 16 2022 Devrim Gündüz <devrim@gunduz.org> - 3.5.0-1
- Update to 3.5.0

* Sun Mar 6 2022 Devrim Gündüz <devrim@gunduz.org> - 3.4.0-1
- Update to 3.4.0

* Tue Feb 8 2022 Devrim Gündüz <devrim@gunduz.org> - 3.3.1-1
- Update to 3.3.1

* Mon Sep 13 2021 Devrim Gündüz <devrim@gunduz.org> - 3.2.0-1
- Update to 3.2.0

* Fri Sep 27 2019 Devrim Gündüz <devrim@gunduz.org> - 2.1.1-1
- Update to 2.1.1

* Tue Apr 16 2019 Devrim Gündüz <devrim@gunduz.org> - 2.1.0-1
- Update to 2.1.0

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 1.6.0-1.1
- Rebuild against PostgreSQL 11.0

* Tue Jun 6 2017 Devrim Gündüz <devrim@gunduz.org> 1.6.0-1
- Update to 1.6.0

* Mon Sep 19 2016 Devrim Gündüz <devrim@gunduz.org> 1.2.0-1
- Update to 1.2.0
- Fix packaging errors, spec file errors, etc.

* Fri Apr 17 2015 Devrim Gündüz <devrim@gunduz.org> 0.16.3-1
- Initial packaging for PostgreSQL YUM repository.
