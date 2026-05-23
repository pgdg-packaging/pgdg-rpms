# generate/package docs
%global	docs 1

# define to enable verbose build for debugging
%global	sbcl_verbose 0
%global	sbcl_shell /bin/bash

Name:		sbcl
Summary:	Steel Bank Common Lisp
Version:	2.2.10
Release:	3%{?dist}

License:	BSD
URL:		http://sbcl.sourceforge.net/
Source0:	http://downloads.sourceforge.net/sourceforge/sbcl/sbcl-%{version}-source.tar.bz2

ExclusiveArch:	%{arm} %{ix86} x86_64 ppc sparcv9 aarch64

# Pre-generated html docs
Source1:	http://downloads.sourceforge.net/sourceforge/sbcl/sbcl-%{version}-documentation-html.tar.bz2

## x86_64 section
Source20:	http://downloads.sourceforge.net/sourceforge/sbcl/sbcl-2.0.11-x86-64-linux-binary.tar.bz2
%ifarch x86_64
%global		sbcl_arch x86-64
# or
%global		sbcl_bootstrap_src -b 20
%global		sbcl_bootstrap_dir sbcl-2.0.11-x86-64-linux
%endif

## ppc section
# Thanks David!
%ifarch ppc
%global		sbcl_arch ppc
BuildRequires:	sbcl
# or
#Source30: sbcl-1.0.1-patched_el4-powerpc-linux.tar.bz2
#Source30: sbcl-1.0.1-patched-powerpc-linux.tar.bz2
%endif

## sparc section
%ifarch sparcv9
%global		sbcl_archsparc
BuildRequires:	sbcl
# or
#Source40: http://downloads.sourceforge.net/sourceforge/sbcl/sbcl-0.9.17-sparc-linux-binary.tar.bz2
%endif

## arm section
%ifarch armv5tel
%global		sbcl_arch arm
BuildRequires:	sbcl
# or
#Source50: http://downloads.sourceforge.net/sourceforge/sbcl/sbcl-1.2.0-armel-linux-binary.tar.bz2
%endif

# generated on a fedora20 arm box, sf bootstrap missing sb-gmp
%ifarch armv6hl armv7hl
%global		sbcl_arch arm
BuildRequires:	sbcl
# or
#Source60: sbcl-1.2.0-armhf-linux-binary-2.tar.bz2
#Source60: http://downloads.sourceforge.net/sourceforge/sbcl/sbcl-1.2.0-armhf-linux-binary.tar.bz2
%endif

## aarch64 section
%ifarch aarch64
%global		sbcl_arch arm64
BuildRequires:	sbcl
# or
#Source70: http://downloads.sourceforge.net/sourceforge/sbcl/sbcl-1.3.16-arm64-linux-binary.tar.bz2
%endif

BuildRequires:	make
BuildRequires:	libzstd-devel
%if 0%{?fedora} >= 35
BuildRequires:	ctags
%endif
%if 0%{?el8}
BuildRequires:	ctags-etags
%endif
BuildRequires:	gcc
BuildRequires:	zlib-devel
%if 0%{?docs}
# doc generation
BuildRequires:	ghostscript
BuildRequires:	texinfo
BuildRequires:	time
%endif

%description
Steel Bank Common Lisp (SBCL) is a Open Source development environment
for Common Lisp. It includes an integrated native compiler,
interpreter, and debugger.


%prep
%setup -q -c -n sbcl-%{version} -a 1 %{?sbcl_bootstrap_src}

pushd sbcl-%{version}

# fix permissions (some have eXecute bit set)
find . -name '*.c' | xargs chmod 644

# set version.lisp-expr
sed -i.rpmver -e "s|\"%{version}\"|\"%{version}-%{release}\"|" version.lisp-expr

# make %%doc items available in parent dir to make life easier
%{__cp} -alf BUGS COPYING README CREDITS NEWS TLA TODO PRINCIPLES ..
%{__ln_s} sbcl-%{version}/doc ../doc
popd

%build
# LTO causes testsuite failures, though it may be the case that the tests are racy.
# Until further analysis is complete, disable LTO
%global _lto_cflags %{nil}

pushd sbcl-%{version}

export CFLAGS="%{?optflags}"
export LDFLAGS="%{?__global_ldflags}"
export CC=gcc

export SBCL_HOME=%{_prefix}/lib/sbcl
%{?sbcl_arch:export SBCL_ARCH=%{sbcl_arch}}
%{?sbcl_shell} \
./make.sh \
  --prefix=%{_prefix} \
  --with-sb-core-compression \
  %{?sbcl_bootstrap_dir:--xc-host="`pwd`/../../%{sbcl_bootstrap_dir}/run-sbcl.sh"}

# docs
%if 0%{?docs}
make -C doc/manual info

# Handle pre-generated docs
tar xvjf %{SOURCE1}
%{__cp} -av %{name}-%{version}/doc/manual/* doc/manual/
%endif
popd


%install
pushd sbcl-%{version}
mkdir -p %{buildroot}{%{_bindir},%{_prefix}/lib,%{_mandir}}

unset SBCL_HOME
export INSTALL_ROOT=%{buildroot}%{_prefix}
%{?sbcl_shell} ./install.sh

popd

## Unpackaged files
rm -rfv %{buildroot}%{_docdir}/sbcl
rm -fv %{buildroot}%{_infodir}/dir
# CVS crud
find %{buildroot} -name CVS -type d | xargs rm -rfv
find %{buildroot} -name .cvsignore | xargs rm -fv

%files
%license COPYING
%doc BUGS CREDITS NEWS PRINCIPLES README TLA TODO
%{_bindir}/sbcl
%dir %{_prefix}/lib/sbcl/
%{_prefix}/lib/sbcl/sbcl.mk
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
* Sat May 23 2026 Devrim Gunduz <devrim@gunduz.org> - 2.2.10-3PGDG
- Remove self-BR dependency.

* Thu May 7 2026 Devrim Gunduz <devrim@gunduz.org> - 2.2.10-2PGDG
- Remove %%check section to cut build times.

* Thu Nov 3 2022 Devrim Gunduz <devrim@gunduz.org> - 2.2.10-1
- Initial packaging for the PostgreSQL RPM repository to support
  pgloader dependency. Spec file written by Stephen Hassard
  <steve@hassard.net>, and I fixed a few rpmlint warnings.

