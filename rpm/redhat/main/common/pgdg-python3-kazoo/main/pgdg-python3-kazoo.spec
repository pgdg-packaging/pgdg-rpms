%global	modname kazoo

# This spec builds one flavor, depending on the distribution:
#
# - the python3.12 / python311 alt-stack flavor (python3.12-kazoo on RHEL 8
#   and RHEL 9, python311-kazoo on SLES), for Patroni,
# - the default python3 flavor (python3-kazoo and python3-kazoo-doc) on
#   RHEL 10 and Amazon Linux 2023. This used to be the separate python3-kazoo
#   directory, merged here per
#   https://github.com/pgdg-packaging/pgdg-rpms/issues/369
%global	pgdg_altstack 0
%if 0%{?rhel} && 0%{?rhel} <= 9
%global	pgdg_altstack 1
%global	alt_pyver 3.12
%global	alt_pkgversion 3.12
%endif
%if 0%{?suse_version} >= 1500
%global	pgdg_altstack 1
%global	alt_pyver 3.11
%global	alt_pkgversion 311
%endif

%if %{pgdg_altstack}
%global	alt_python %{_bindir}/python%{alt_pyver}
%global	alt_sitelib %{_prefix}/lib/python%{alt_pyver}/site-packages
Name:		python%{alt_pkgversion}-%{modname}
%else
Name:		python3-%{modname}
%endif
Version:	2.11.0
Release:	3PGDG%{?dist}
Summary:	Higher level Python Zookeeper client

License:	Apache-2.0
URL:		https://kazoo.readthedocs.org
Source0:	https://pypi.python.org/packages/source/k/%{modname}/%{modname}-%{version}.tar.gz
BuildArch:	noarch

%if %{pgdg_altstack}
BuildRequires:	python%{alt_pkgversion}-devel
BuildRequires:	python%{alt_pkgversion}-setuptools
%else
BuildRequires:	python3-sphinx
BuildRequires:	python3-devel
BuildRequires:	python3-pip
BuildRequires:	python3-setuptools
BuildRequires:	python3-wheel
BuildRequires:	pyproject-rpm-macros
%endif

%description
Kazoo is a Python library designed to make working with Zookeeper a more\
hassle-free experience that is less prone to errors.

%if ! %{pgdg_altstack}
%package doc
Summary:	Documentation for %{name}

%description doc
Kazoo is a Python library designed to make working with Zookeeper a more
hassle-free experience that is less prone to errors.

This package contains documentation in HTML format.
%endif

%prep
%setup -q -n %{modname}-%{version}
# Remove bundled egg-info
%{__rm} -rf %{modname}.egg-info

find . -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python3}|'

%if ! %{pgdg_altstack}
# sphinx_autodoc_typehints isn't packaged for our real targets (EL/AL2023);
# drop it, it only adds type-hint rendering to the docs
sed -i '/^\s*"sphinx_autodoc_typehints",\?\s*$/d' docs/conf.py

# generate html docs
sphinx-build docs html
# remove the sphinx-build leftovers
%{__rm} -rf html/.{doctrees,buildinfo}
%endif

%build
%if %{pgdg_altstack}
%{alt_python} setup.py build
%else
%pyproject_wheel
%endif

%install
%if %{pgdg_altstack}
%{alt_python} setup.py install --no-compile --root %{buildroot}
#delete tests
%{__rm} -fr %{buildroot}%{alt_sitelib}/%{modname}/tests/
%else
%pyproject_install
#delete tests
%{__rm} -fr %{buildroot}%{python3_sitelib}/%{modname}/tests/
%endif

%files
%doc README.md LICENSE
%if %{pgdg_altstack}
%{alt_sitelib}/%{modname}
%{alt_sitelib}/%{modname}-%{version}-py%{alt_pyver}.egg-info
%else
%{python3_sitelib}/%{modname}
%{python3_sitelib}/%{modname}-%{version}.dist-info/

%files doc
%doc html
%endif

%changelog
* Tue Oct 13 2026 Devrim Gunduz <devrim@gunduz.org> - 2.11.0-3PGDG
- Merge the python3-kazoo spec (default python3 flavor) into this one:
  build python3.12-kazoo on RHEL 8 and RHEL 9 and python311-kazoo on SLES as
  before, and python3-kazoo (and -doc) on RHEL 10 and Amazon Linux 2023, as
  python3-kazoo did. Drop python3-kazoo on RHEL 8 and RHEL 9: nothing uses
  it (Patroni uses python3.12-kazoo there), and it did not build on RHEL 8
  since the switch to pyproject builds. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/369

* Mon Sep 14 2026 Devrim Gündüz <devrim@gunduz.org> - 2.11.0-2
- Drop the sphinx_autodoc_typehints Sphinx extension from docs/conf.py in
  %%prep: it's not packaged for RHEL/AL2023, and docs build fail.
- Switch to pyproject builds

* Fri Sep 11 2026 Devrim Gunduz <devrim@gunduz.org> - 2.11.0-2PGDG
- Remove Fedora <= 42 support
- Add missing Fedora 44 pin (python3.14)

* Mon Aug 31 2026 Devrim Gündüz <devrim@gunduz.org> - 2.11.0-1
- Update to 2.11.0 per changes described at:
  https://pypi.org/project/kazoo/2.11.0/

* Mon Aug 31 2026 Devrim Gunduz <devrim@gunduz.org> - 2.11.0-1PGDG.1
- Update to 2.11.0 per changes described at:
  https://pypi.org/project/kazoo/2.11.0/

* Tue Aug 25 2026 Devrim Gunduz <devrim@gunduz.org> - 2.8.0-44PGDG.1
- Explicitly bytecompile with %%py_byte_compile on Amazon Linux 2023.
  AL2023's brp-python-bytecompile doesn't auto-discover the python3.13
  alt-stack site-packages dir, so __pycache__ was never populated.

* Tue Aug 25 2026 Devrim Gunduz <devrim@gunduz.org> - 2.8.0-43PGDG.1
- Build against the python3.13 alt-stack on Amazon Linux 2023, to keep
  the Python stack consistent across all packages in the repo.

* Mon Sep 22 2025 Devrim Gunduz <devrim@gunduz.org> - 2.8.0-42PGDG.1
- Add Fedora 43 support

* Tue May 20 2025 Devrim Gunduz <devrim@gunduz.org> - 2.8.0-42PGDG
- Initial packaging for the PostgreSQL RPM repository to support Patroni
  on RHEL 9 and 8 and SLES 15.

* Wed Aug 5 2020 Devrim Gündüz <devrim@gunduz.org> - 2.8.0-1
- Initial packaging for the PostgreSQL RPM repository, to satisfy patroni
  dependency on RHEL 8, based on Fedora rawhide spec file.
