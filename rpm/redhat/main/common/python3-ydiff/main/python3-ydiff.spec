Name:		ydiff
Version:	1.4.2
Release:	43PGDG%{?dist}
Summary:	View colored, incremental diff
URL:		https://github.com/ymattw/ydiff
License:	BSD
Source0:	https://github.com/ymattw/ydiff/archive/%{version}/%{name}-%{version}.tar.gz
BuildRequires:	python3-devel
BuildArch:	noarch

Requires:	less
Requires:	python%{python3_pkgversion}-%{name}
%description
Term based tool to view colored, incremental diff in a Git/Mercurial/Svn
workspace or from stdin, with side by side (similar to diff -y) and auto
pager support.

%package -n	python3-%{name}
Summary:	%{summary}
%if 0%{?fedora} >= 40 || 0%{?rhel} >= 9 || 0%{?suse_version} >= 1500
%{?python_provide:%python_provide python3-%{name}}
%endif
%description -n	python3-%{name}
Python library that implements API used by ydiff tool.

%prep
%autosetup -n %{name}-%{version}
/usr/bin/sed -i '/#!\/usr\/bin\/env python/d' ydiff.py

%build
%py3_build

%install
%py3_install

%files
%doc README.rst
%license LICENSE
%{_bindir}/ydiff

%files -n python3-%{name}
%{python3_sitelib}/__pycache__/*
%{python3_sitelib}/%{name}.py
%{python3_sitelib}/%{name}-%{version}-py%{python3_version}.egg-info

%changelog
* Sat Apr 19 2025 Devrim Gündüz <devrim@gunduz.org> - 1.4.2-43PGDG
- Rebuild on RHEL 8 because of an issue on the build instance

* Thu Apr 17 2025 Devrim Gündüz <devrim@gunduz.org> - 1.4.2-42PGDG
- Update to 1.4.2

* Wed Feb 21 2024 Devrim Gündüz <devrim@gunduz.org> - 1.2-11PGDG
- Add PGDG branding

* Thu Oct 1 2020 Devrim Gündüz <devrim@gunduz.org> - 1.2-10
- Initial packaging for the PostgreSQL RPM repository to satisfy Patroni
  dependency. Took the spec file from Fedora rawhide.
