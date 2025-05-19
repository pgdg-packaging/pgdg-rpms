%global modname argcomplete

%if 0%{?fedora} && 0%{?fedora} <= 42
%global	__python3 %{_bindir}/python3.13
%global	python3_pkgversion 3.13
%endif
%if 0%{?rhel} && 0%{?rhel} < 10
%global	__python3 %{_bindir}/python3.12
%global	python3_pkgversion 3.12
%endif
%if 0%{?suse_version} >= 1500
%global	__python3 %{_bindir}/python3.11
%global	python3_pkgversion 311
%endif

Name:		python%{python3_pkgversion}-%{modname}
Summary:	Bash tab completion for argparse
Version:	3.6.2
Release:	1PGDG%{dist}
License:	Apache-2.0
URL:		https://github.com/kislyuk/%{modname}
Source0:	https://files.pythonhosted.org/packages/source/a/%{modname}/%{modname}-%{version}.tar.gz

# Temporary hotfix for https://bugzilla.redhat.com/2359689
# Reported upstream in https://github.com/kislyuk/argcomplete/issues/535
Patch:         hotfix-bz2359689.patch

BuildRequires: python%{python3_pkgversion}-devel
BuildArch:     noarch

%description
Tab complete all the things!

Argcomplete provides easy, extensible command line tab completion of
arguments for your Python application.

It makes two assumptions:

 - You're using bash or zsh as your shell
 - You're using argparse to manage your command line arguments/options

Argcomplete is particularly useful if your program has lots of options
or subparsers, and if your program can dynamically suggest completions
for your argument/option values (for example, if the user is browsing
resources over the network).}

%prep
%autosetup -p1 -n argcomplete-%{version}
# Remove useless BRs (aka linters)
sed -i -r -e '/test = /s/"(coverage|ruff|mypy)"[, ]*//g' pyproject.toml

# https://github.com/kislyuk/argcomplete/issues/255
# https://github.com/kislyuk/argcomplete/issues/256
sed -i -e "1s|#!.*python.*|#!%{__python3}|" test/prog argcomplete/scripts/*
sed -i -e "s|python |python3 |" test/test.py

# Remove shebang from installed scripts
sed -i '/^#!/d' argcomplete/scripts/*.py

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%{__rm} %{buildroot}%{_bindir}/*

%files
%license LICENSE.rst
%doc README.rst
%{python3_sitelib}/%{modname}-%{version}.dist-info/*
%{python3_sitelib}/argcomplete/*.py*
%{python3_sitelib}/argcomplete/__pycache__/*.py*
%{python3_sitelib}/argcomplete/bash_completion.d/_python-argcomplete
%{python3_sitelib}/argcomplete/packages/*.py*
%{python3_sitelib}/argcomplete/packages/__pycache__/*.py*
%{python3_sitelib}/argcomplete/py.typed
%{python3_sitelib}/argcomplete/scripts/*.py*
%{python3_sitelib}/argcomplete/scripts/__pycache__/*.py*

%changelog
* Mon May 19 2025 Devrim Gunduz <devrim@gunduz.org> - 3.6.2-1PGDG
- Inıtial packaging for the PostgreSQL RPM repository to support Barman
  on RHEL 9 and RHEL 8. Modified Fedora rawhide spec file.
