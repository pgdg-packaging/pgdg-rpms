# generate/package docs
%global	docs 1

%global	sbcl_shell /bin/bash

# The test suite is long; run it with --define 'runselftest 1'.
%{!?runselftest:%global runselftest 0}

# Only x86_64 can be built: upstream ships Linux bootstrap binaries for
# x86-64 only, and there is no Lisp for other architectures in RHEL or EPEL.
%global	sbcl_arch x86-64
%global	sbcl_bootstrap_ver 2.0.11
%global	sbcl_bootstrap_dir sbcl-%{sbcl_bootstrap_ver}-x86-64-linux

Name:		sbcl
Summary:	Steel Bank Common Lisp
Version:	2.6.10
Release:	1PGDG%{?dist}

# See COPYING for a license breakdown
License:	LicenseRef-Fedora-Public-Domain AND LOOP AND BSD-3-Clause
URL:		https://sbcl.sourceforge.io/
Source0:	https://downloads.sourceforge.net/sourceforge/%{name}/%{name}-%{version}-source.tar.bz2
Source20:	https://downloads.sourceforge.net/sourceforge/%{name}/%{name}-%{sbcl_bootstrap_ver}-x86-64-linux-binary.tar.bz2

# Patches from Fedora
Patch1:		sbcl-0001-Do-not-modify-CFLAGS.patch
Patch2:		sbcl-0002-Fix-for-mock-builds-when-proc-isn-t-available.patch
Patch3:		sbcl-0003-Verbose-build.patch
Patch4:		sbcl-0004-fix-install.sh-use-basename-when-installing-LIBSBCL-.patch

ExclusiveArch:	x86_64

BuildRequires:	make
BuildRequires:	gcc
BuildRequires:	libzstd-devel
%if 0%{?fedora} >= 42
BuildRequires:	ctags
%endif
%if 0%{?el8}
BuildRequires:	ctags-etags
%endif
%if 0%{?docs}
# doc generation
BuildRequires:	texinfo
BuildRequires:	time
%endif
%if %runselftest
BuildRequires:	ed
BuildRequires:	hostname
BuildRequires:	strace
%endif

%description
Steel Bank Common Lisp (SBCL) is a Open Source development environment
for Common Lisp. It includes an integrated native compiler,
interpreter, and debugger.

%prep
%autosetup -p1

# Bootstrap binary goes outside the source tree
tar -xjf %{SOURCE20} -C ..

# set version.lisp-expr
sed -i.rpmver -e "s|\"%{version}\"|\"%{version}-%{release}\"|" version.lisp-expr

%build
# LTO breaks the runtime link on RHEL 9/10 and AL2023: undefined
# reference to call_into_lisp_ (an assembly symbol).
%global _lto_cflags %{nil}

export CFLAGS='%{build_cflags}'
export LDFLAGS='%{build_ldflags}'
export CC=gcc

export SBCL_HOME=%{_prefix}/lib/sbcl
export SBCL_ARCH=%{sbcl_arch}
%{?sbcl_shell} \
./make.sh \
  --fancy \
  --prefix=%{_prefix} \
  --with-sb-core-compression \
  --with-sb-linkable-runtime \
  --xc-host="$(pwd)/../%{sbcl_bootstrap_dir}/run-sbcl.sh"

# docs
%if 0%{?docs}
%{__make} -C doc/manual html info
%endif

%install
mkdir -p %{buildroot}{%{_bindir},%{_prefix}/lib,%{_mandir}}

unset SBCL_HOME
export INSTALL_ROOT=%{buildroot}%{_prefix}
%{?sbcl_shell} ./install.sh

## Unpackaged files
rm -rfv %{buildroot}%{_docdir}/sbcl
rm -fv  %{buildroot}%{_infodir}/dir
# CVS crud
find %{buildroot} -name .cvsignore -delete
# 'test-passed' files from %%check
find %{buildroot} -name 'test-passed' -delete

%check
ERROR=0
# sanity check, essential contrib modules get built/included?
CONTRIBS="sb-posix.fasl sb-bsd-sockets.fasl"
for CONTRIB in $CONTRIBS ; do
  if [ ! -f %{buildroot}%{_prefix}/lib/sbcl/contrib/$CONTRIB ]; then
    echo "WARNING: ${CONTRIB} awol!"
    ERROR=1
    echo "ulimit -a"
    ulimit -a
  fi
done
%if %runselftest
pushd tests
# still seeing Failure: threads.impure.lisp / (DEBUGGER-NO-HANG-ON-SESSION-LOCK-IF-INTERRUPTED)
time %{?sbcl_shell} ./run-tests.sh ||:
popd
%endif
exit $ERROR

%files
%license COPYING
%doc BUGS CREDITS NEWS PRINCIPLES README TLA TODO
%{_bindir}/sbcl
%dir %{_prefix}/lib/sbcl/
%{_prefix}/lib/sbcl/sbcl.mk
%{_prefix}/lib/sbcl/sbcl.o
%{_prefix}/lib/sbcl/contrib/
%{_mandir}/man1/sbcl.1*
%if 0%{?docs}
%doc doc/manual/sbcl.html
%doc doc/manual/asdf.html
%{_infodir}/asdf.info*
%{_infodir}/sbcl.info*
%endif
%{_prefix}/lib/sbcl/sbcl.core

%changelog
* Thu Nov 19 2026 Devrim Gunduz <devrim@gunduz.org> - 2.6.10-1PGDG
- Update to 2.6.10 per changes described at:
  https://www.sbcl.org/news.html
- Sync with the Fedora spec file: add Fedora's patches (do not modify
  CFLAGS, mock builds without /proc, verbose build, install.sh fix for
  the linkable runtime), build with --fancy and the linkable runtime
  (ships sbcl.o), use the Fedora build flags (still without LTO), SPDX
  license tag, and build the HTML and info manuals from the source
  instead of downloading the pre-generated HTML docs.
- Add back a %%check section: the contrib sanity check always runs, the
  full test suite only with runselftest 1.
- Restrict the build to x86_64, the only architecture with an upstream
  bootstrap binary, and drop the dead per-architecture sections.

* Mon Aug 31 2026 Devrim Gunduz <devrim@gunduz.org> - 2.6.8-1PGDG
- Update to 2.6.8 per changes described at:
  https://www.sbcl.org/news.html

* Sat May 23 2026 Devrim Gunduz <devrim@gunduz.org> - 2.2.10-3PGDG
- Remove self-BR dependency.

* Thu May 7 2026 Devrim Gunduz <devrim@gunduz.org> - 2.2.10-2PGDG
- Remove %%check section to cut build times.

* Thu Nov 3 2022 Devrim Gunduz <devrim@gunduz.org> - 2.2.10-1
- Initial packaging for the PostgreSQL RPM repository to support
  pgloader dependency. Spec file written by Stephen Hassard
  <steve@hassard.net>, and I fixed a few rpmlint warnings.
