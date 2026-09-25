#!/usr/bin/bash

set -euo pipefail

if [ $# -lt 1 ]; then
	echo "Usage: $0 version"
	exit 1
fi

VERSION="$1"
TOPDIR="$PWD"
WORKDIR="$TOPDIR/tmp/anon-$VERSION"

mkdir -p "$WORKDIR" && cd "$WORKDIR"
curl -LO https://gitlab.com/dalibo/postgresql_anonymizer/-/archive/$VERSION/postgresql_anonymizer-$VERSION.tar.gz
tar xf postgresql_anonymizer-$VERSION.tar.gz
cd postgresql_anonymizer-$VERSION/
# Keep the crate cache and the temporary files out of the source tree and /tmp:
export CARGO_HOME="$WORKDIR/cargo-home" TMPDIR="$WORKDIR/tmp"
mkdir -p "$TMPDIR"
cargo vendor vendor
tar --sort=name --mtime=@0 --owner=0 --group=0 --numeric-owner -cf - vendor | xz -T0 -6 > "$WORKDIR/postgresql_anonymizer-$VERSION-vendor.tar.xz"
xz -t "$WORKDIR/postgresql_anonymizer-$VERSION-vendor.tar.xz"

mv "$WORKDIR/postgresql_anonymizer-$VERSION-vendor.tar.xz" "$TOPDIR/"
cd "$TOPDIR"
rm -rf "$TOPDIR/tmp"
