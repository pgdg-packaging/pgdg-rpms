#!/usr/bin/bash

set -euo pipefail

if [ $# -lt 1 ]; then
	echo "Usage: $0 version"
	exit 1
fi

VERSION="$1"
TOPDIR="$PWD"
WORKDIR="$TOPDIR/tmp/pydantic_core-$VERSION"

mkdir -p "$WORKDIR" && cd "$WORKDIR"
curl -Lo pydantic_core-$VERSION.tar.gz https://files.pythonhosted.org/packages/source/p/pydantic_core/pydantic_core-$VERSION.tar.gz
tar xf pydantic_core-$VERSION.tar.gz
cd pydantic_core-$VERSION/
# Keep the crate cache and the temporary files out of the source tree and /tmp:
export CARGO_HOME="$WORKDIR/cargo-home" TMPDIR="$WORKDIR/tmp"
mkdir -p "$TMPDIR"
# Only keep the crates for the Linux architectures that we build on, and not
# the dev dependencies. The other crates are replaced with empty stubs, so that
# Cargo.lock still resolves. Needs cargo-vendor-filterer.
cargo vendor-filterer \
	--platform=x86_64-unknown-linux-gnu \
	--platform=aarch64-unknown-linux-gnu \
	--platform=powerpc64le-unknown-linux-gnu \
	--platform=s390x-unknown-linux-gnu \
	--keep-dep-kinds=no-dev vendor
tar --sort=name --mtime=@0 --owner=0 --group=0 --numeric-owner -cf - vendor | xz -T0 -6 > "$WORKDIR/pydantic_core-$VERSION-vendor.tar.xz"
xz -t "$WORKDIR/pydantic_core-$VERSION-vendor.tar.xz"

mv "$WORKDIR/pydantic_core-$VERSION-vendor.tar.xz" "$TOPDIR/"
cd "$TOPDIR"
rm -rf "$TOPDIR/tmp"
