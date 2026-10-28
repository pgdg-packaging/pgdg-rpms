%pgdg_python3_setup

%global modname daemonize

%{expand: %%global py3ver %(echo `%{__python3} -c "import sys; sys.stdout.write(sys.version[:4])"`)}
%global python3_sitelib %(%{__python3} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")

Name:		python%{python3_pkgversion}-%{modname}
Version:	2.5.0
Release:	44PGDG%{?dist}
Summary:	Library for writing system daemons in Python

License:	MIT
URL:		https://github.com/thesharp/%{modname}
Source0:	%{url}/archive/v%{version}/%{modname}-%{version}.tar.gz

BuildArch:	noarch

BuildRequires:	python%{python3_pkgversion}-devel

%description
daemonize is a library for writing system daemons in Python.

%prep
%autosetup -n %{modname}-%{version}

%build
%{__python3} setup.py build

%install
%{__python3} setup.py install --no-compile --root %{buildroot}

%files
%license LICENSE
%doc README.rst
%{python3_sitelib}/%{modname}-*.egg-info/
%{python3_sitelib}/%{modname}.py
%if 0%{?fedora} >= 41 || 0%{?rhel} >= 9
%{python3_sitelib}/__pycache__/%{modname}.*
%endif

%changelog
* Wed Oct 28 2026 Devrim Gündüz <devrim@gunduz.org> - 2.5.0-44PGDG
- Use %%pgdg_python3_setup from pgdg-srpm-macros 2.5.0 instead of the
  per-distro Python block and the __ospython macro. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/462

* Tue Aug 25 2026 Devrim Gündüz <devrim@gunduz.org> - 2.5.0-43
- Build against the python3.13 alt-stack on Amazon Linux 2023, to keep
  the Python stack consistent across all packages in the repo.

* Sat Mar 28 2026 Devrim Gündüz <devrim@gunduz.org> - 2.5.0-42
- Add to SLES

* Thu Dec 10 2020 Devrim Gündüz <devrim@gunduz.org> - 2.5.0-8
- Initial packaging to satisfy pg_chameleon dependency on
  RHEL 7 and 8.
