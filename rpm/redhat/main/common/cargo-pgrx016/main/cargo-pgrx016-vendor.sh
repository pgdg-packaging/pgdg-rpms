#!/usr/bin/bash

set -euo pipefail

if [ $# -lt 1 ]; then
	echo "Usage: $0 version"
	exit 1
fi

VERSION="$1"
# The openssl crates that %prep switches Cargo.lock to (the versions that
# cargo-pgrx 0.19.1 uses), as the ones in Cargo.lock of this release do not
# build with OpenSSL 4:
OPENSSL_VERSION="0.10.80"
OPENSSL_SYS_VERSION="0.9.116"
TOPDIR="$PWD"
WORKDIR="$TOPDIR/tmp/cargo-pgrx-$VERSION"

mkdir -p "$WORKDIR" && cd "$WORKDIR"
curl -Lo cargo-pgrx-$VERSION.crate https://static.crates.io/crates/cargo-pgrx/cargo-pgrx-$VERSION.crate
tar xf cargo-pgrx-$VERSION.crate
cd cargo-pgrx-$VERSION/
# Keep the crate cache and the temporary files out of the source tree and /tmp:
export CARGO_HOME="$WORKDIR/cargo-home" TMPDIR="$WORKDIR/tmp"
mkdir -p "$TMPDIR"
# Vendor the newer openssl crates too, with an empty crate that depends on
# them, so that "cargo update --offline" in %prep finds them:
mkdir -p "$WORKDIR/openssl-new/src"
touch "$WORKDIR/openssl-new/src/lib.rs"
cat > "$WORKDIR/openssl-new/Cargo.toml" <<CARGOEOF
[package]
name = "openssl-new"
version = "0.0.0"
edition = "2021"

[dependencies]
openssl = "=$OPENSSL_VERSION"
openssl-sys = "=$OPENSSL_SYS_VERSION"
CARGOEOF
# Only keep the crates for the Linux architectures that we build on, and not the
# dev dependencies. The other crates are replaced with empty stubs, so that
# Cargo.lock still resolves. Needs cargo-vendor-filterer. ('*-unknown-linux-gnu'
# does not work, as the LLVM of Fedora cannot create a target machine for m68k.)
cargo vendor-filterer \
	--platform=x86_64-unknown-linux-gnu \
	--platform=aarch64-unknown-linux-gnu \
	--platform=powerpc64le-unknown-linux-gnu \
	--platform=s390x-unknown-linux-gnu \
	--sync="$WORKDIR/openssl-new/Cargo.toml" \
	--all-features --keep-dep-kinds=no-dev vendor
tar --sort=name --mtime=@0 --owner=0 --group=0 --numeric-owner -cf - vendor | xz -T0 -6 > "$WORKDIR/cargo-pgrx-$VERSION-vendor.tar.xz"
xz -t "$WORKDIR/cargo-pgrx-$VERSION-vendor.tar.xz"

mv "$WORKDIR/cargo-pgrx-$VERSION-vendor.tar.xz" "$TOPDIR/"
cd "$TOPDIR"
rm -rf "$TOPDIR/tmp"
