# The pyproject-rpm-macros line that upstream maintains for RHEL 8 (the epel8
# branch of the Fedora package), which works with the RPM version of RHEL 8.
# The installed files are identical to the ones of the EPEL package, so both
# can be installed at the same time.
Name:		pgdg-pyproject-rpm-macros
Summary:	PGDG RPM macros for PEP 517 Python packages (minimal)
License:	MIT
# 1.9.0 (from Fedora rawhide) was released before; this line is versioned
# 0.1.x upstream:
Epoch:		1
Version:	0.1.12.0
Release:	1PGDG%{?dist}
URL:		https://src.fedoraproject.org/rpms/pyproject-rpm-macros
# From https://src.fedoraproject.org/rpms/pyproject-rpm-macros/tree/epel8
# Macro files
Source001:	macros.pyproject
# Implementation files
Source102:	pyproject_save_files.py
Source104:	pyproject_preprocess_record.py
Source107:	pyproject_wheel.py
# Metadata
Source901:	README.md
Source902:	LICENSE

BuildArch:	noarch

# The spec files of the PostgreSQL RPM repository BuildRequire
# pyproject-rpm-macros, which is only in EPEL on RHEL 8. This package
# provides it, without replacing the EPEL package:
Provides:	pyproject-rpm-macros = %{version}
# 1.9.0 had this subpackage; this line has no %%pyproject_buildrequires, as
# RHEL 8 has no dynamic BuildRequires:
Obsoletes:	pgdg-pyproject-srpm-macros <= 1.9.0

# We build on top of those:
Requires:	python-rpm-macros
Requires:	python-srpm-macros
Requires:	python3-rpm-macros
# This package is incompatible with python36.
# We use rich dependencies to avoid creating implicit conflicts between
# python3X-devel.
Requires:	(python38-rpm-macros or python39-rpm-macros or python3.11-rpm-macros or python3.12-rpm-macros)
Suggests:	(python38-rpm-macros if python38-devel)
Suggests:	(python39-rpm-macros if python39-devel)
Suggests:	(python3.11-rpm-macros if python3.11-devel)
Suggests:	(python3.12-rpm-macros if python3.12-devel)

# We use the following tools outside of coreutils
Requires:	/usr/bin/find
Requires:	/usr/bin/sed

# These packages are pulled in unconditionally by %%pyproject_buildrequires
# on Fedora, so we Require them here.
Requires:	(python38-devel if python38-rpm-macros)
Requires:	(python39-devel if python39-rpm-macros)
Requires:	(python3.11-devel if python3.11-rpm-macros)
Requires:	(python3.12-devel if python3.12-rpm-macros)

Requires:	(python3.8dist(pip) if python38-rpm-macros)
Requires:	(python3.9dist(pip) if python39-rpm-macros)
Requires:	(python3.11dist(pip) if python3.11-rpm-macros)
Requires:	(python3.12dist(pip) if python3.12-rpm-macros)

%description
These macros allow projects that follow the Python packaging specifications
to be packaged as RPMs in the PostgreSQL RPM repository.

They work for:

* traditional Setuptools-based projects that use the setup.py file,
* newer Setuptools-based projects that have a setup.cfg file,
* general Python projects that use the PEP 517 pyproject.toml file
  (which allows using any build system, such as setuptools, flit or poetry).

These macros replace %%py3_build and %%py3_install,
which only work with setup.py.

This is a slimmed down version of the macros that are available in Fedora,
in order to be compatible with el8's RPM version.
Notably, %%tox and %%pyproject_buildrequires are absent, so buildrequirements
must be manually specified. It is only compatible with python38+.

%prep
# Not strictly necessary but allows working on file names instead
# of source numbers in install section
%setup -c -T
%{__cp} -p %{sources} .

%build
# nothing to do, sources are not buildable

%install
%{__mkdir} -p %{buildroot}%{_rpmmacrodir}
%{__mkdir} -p %{buildroot}%{_rpmconfigdir}/redhat
%{__install} -pm 644 macros.pyproject %{buildroot}%{_rpmmacrodir}/
%{__install} -pm 644 pyproject_save_files.py %{buildroot}%{_rpmconfigdir}/redhat/
%{__install} -pm 644 pyproject_preprocess_record.py %{buildroot}%{_rpmconfigdir}/redhat/
%{__install} -pm 644 pyproject_wheel.py %{buildroot}%{_rpmconfigdir}/redhat/

%files
%{_rpmmacrodir}/macros.pyproject
%{_rpmconfigdir}/redhat/pyproject_save_files.py
%{_rpmconfigdir}/redhat/pyproject_preprocess_record.py
%{_rpmconfigdir}/redhat/pyproject_wheel.py
%doc README.md
%license LICENSE

%changelog
* Fri Oct 23 2026 Devrim Gündüz <devrim@gunduz.org> - 1:0.1.12.0-1PGDG
- Switch to the pyproject-rpm-macros line that upstream maintains for
  RHEL 8 (the epel8 branch of the Fedora package): 1.9.0 from Fedora rawhide
  needs a newer RPM in places (%%pyproject_save_files), and only works with
  the default Python, which our Python packages do not use on RHEL 8.
  Add an Epoch, as the version goes down.
- Provide pyproject-rpm-macros, so that the Python packages that
  BuildRequire it do not need EPEL on RHEL 8. The installed files are
  identical to the ones of the EPEL package, so both can be installed. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/422

* Wed Jul 5 2023 Devrim Gündüz <devrim@gunduz.org> - 1.9.0-1PGDG
* Initial packaging for the PostgreSQL RPM repository. Took spec file
  and other components from Fedora rawhide, and made very little adjustments.
  Currently for RHEL 8 only. These macros are already available on RHEL 9 and
  Fedora.
