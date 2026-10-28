%pgdg_python3_setup

%global	modname websockets

Name:		python%{python3_pkgversion}-%{modname}
Version:	16.1.1
Release:	2PGDG%{?dist}
Summary:	Implementation of the WebSocket Protocol for Python

License:	BSD-3-Clause
URL:		https://github.com/python-websockets/%{modname}
Source0:	https://files.pythonhosted.org/packages/source/w/%{modname}/%{modname}-%{version}.tar.gz

BuildRequires:	python%{python3_pkgversion}-devel
%if ! 0%{?suse_version}
BuildRequires:	pyproject-rpm-macros
%endif
BuildRequires:	python%{python3_pkgversion}-pip
BuildRequires:	python%{python3_pkgversion}-setuptools
BuildRequires:	python%{python3_pkgversion}-wheel
BuildRequires:	gcc

%description
websockets is a library for building WebSocket servers and clients in Python
with a focus on correctness, simplicity, robustness, and performance. It
includes a C extension that speeds up the protocol.

%prep
%autosetup -n %{modname}-%{version}
# PEP 639 license strings need setuptools >= 77, RHEL 9 has 68 and Amazon
# Linux 2023 has 69:
%{__sed} -i 's/^license = "\(.*\)"$/license = { text = "\1" }/' pyproject.toml

%build
%pyproject_wheel

%install
%pyproject_install
# Remove the command line tool, it conflicts with the package of the OS Python:
%{__rm} -rf %{buildroot}%{_bindir}

%files
%license LICENSE
%doc README.rst
%{python3_sitearch}/%{modname}/
%{python3_sitearch}/%{modname}-%{version}.dist-info/

%changelog
* Wed Oct 28 2026 Devrim Gündüz <devrim@gunduz.org> - 16.1.1-2PGDG
- Use %%pgdg_python3_setup from pgdg-srpm-macros 2.5.0 instead of the
  per-distro Python block and the __ospython macro. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/462

* Mon Oct 19 2026 Devrim Gündüz <devrim@gunduz.org> - 16.1.1-1PGDG
- Update to 16.1.1 per changes described at:
  https://websockets.readthedocs.io/en/stable/project/changelog.html
  This is the newest version that google-genai (websockets < 17.0)
  supports. Rewrite the PEP 639 license string in pyproject.toml to the
  old license table, for the setuptools of RHEL 9 and Amazon Linux 2023.
  Per https://github.com/pgdg-packaging/pgdg-rpms/issues/404

* Wed Oct 07 2026 Devrim Gunduz <devrim@gunduz.org> - 15.0.1-1PGDG
- Initial packaging for the PostgreSQL RPM repository, to satisfy
  google-genai dependency (for pg_statviz) on Amazon Linux 2023. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/249
- Add RHEL 9 support (python3.12), for pg_statviz. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/249
