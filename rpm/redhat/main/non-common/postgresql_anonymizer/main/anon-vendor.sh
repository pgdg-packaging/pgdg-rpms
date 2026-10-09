#!/usr/bin/bash

set -euo pipefail

if [ $# -lt 2 ]; then
	echo "Usage: $0 version pgrx_version"
	exit 1
fi

VERSION="$1"
# The pgrx release to build with. It has to be the version of the cargo-pgrx
# package, as cargo-pgrx refuses older pgrx crates:
PGRX_VERSION="$2"
TOPDIR="$PWD"
WORKDIR="$TOPDIR/tmp/anon-$VERSION"

mkdir -p "$WORKDIR" && cd "$WORKDIR"
curl -LO https://gitlab.com/dalibo/postgresql_anonymizer/-/archive/$VERSION/postgresql_anonymizer-$VERSION.tar.gz
tar xf postgresql_anonymizer-$VERSION.tar.gz
cd postgresql_anonymizer-$VERSION/
# Keep the crate cache and the temporary files out of the source tree and /tmp:
export CARGO_HOME="$WORKDIR/cargo-home" TMPDIR="$WORKDIR/tmp"
mkdir -p "$TMPDIR"
# Move the pgrx crates in Cargo.lock to the version of cargo-pgrx. Cargo.lock is
# shipped in the tarball, and replaces the one of upstream in %prep:
cargo update -p pgrx -p pgrx-tests --precise "$PGRX_VERSION"
# Only keep the crates for the Linux architectures that we build on, and not the
# dev dependencies. The other crates are replaced with empty stubs, so that
# Cargo.lock still resolves. Needs cargo-vendor-filterer. ('*-unknown-linux-gnu'
# does not work, as the LLVM of Fedora cannot create a target machine for m68k.)
cargo vendor-filterer \
	--platform=x86_64-unknown-linux-gnu \
	--platform=aarch64-unknown-linux-gnu \
	--platform=powerpc64le-unknown-linux-gnu \
	--platform=s390x-unknown-linux-gnu \
	--all-features --keep-dep-kinds=no-dev vendor
TARBALL="postgresql_anonymizer-$VERSION-pgrx$PGRX_VERSION-vendor.tar.xz"
tar --sort=name --mtime=@0 --owner=0 --group=0 --numeric-owner -cf - Cargo.lock vendor | xz -T0 -6 > "$WORKDIR/$TARBALL"
xz -t "$WORKDIR/$TARBALL"

mv "$WORKDIR/$TARBALL" "$TOPDIR/"
cd "$TOPDIR"
rm -rf "$TOPDIR/tmp"
