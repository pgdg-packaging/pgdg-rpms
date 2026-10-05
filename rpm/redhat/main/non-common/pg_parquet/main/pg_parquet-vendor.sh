#!/usr/bin/bash

set -euo pipefail

if [ $# -lt 1 ]; then
	echo "Usage: $0 version"
	exit 1
fi

VERSION="$1"
# The pgrx version of the cargo-pgrxNNN package that the spec uses. cargo-pgrx
# has to be exactly the same version as the pgrx crate:
PGRX_VERSION="0.16.1"
TOPDIR="$PWD"
WORKDIR="$TOPDIR/tmp/pg_parquet-$VERSION"

mkdir -p "$WORKDIR" && cd "$WORKDIR"
curl -Lo pg_parquet-$VERSION.tar.gz https://github.com/CrunchyData/pg_parquet/archive/refs/tags/v$VERSION.tar.gz
tar xf pg_parquet-$VERSION.tar.gz
cd pg_parquet-$VERSION/
# Keep the crate cache and the temporary files out of the source tree and /tmp:
export CARGO_HOME="$WORKDIR/cargo-home" TMPDIR="$WORKDIR/tmp"
mkdir -p "$TMPDIR"
# Upstream pins pgrx to an exact version. Use the version of our cargo-pgrx
# package instead, and ship the updated Cargo.lock in the tarball next to the
# vendor directory. The spec makes the same change in Cargo.toml:
sed -i -E "s/^(pgrx(-tests)? = )\"=[0-9.]+\"/\1\"=$PGRX_VERSION\"/" Cargo.toml
cargo update -p pgrx -p pgrx-tests --precise $PGRX_VERSION
# pgrx-bindgen 0.16.1 needs bindgen 0.71, which creates opaque structs from the
# PostgreSQL headers with newer clang versions. The spec switches it to bindgen
# 0.72.1 (as pgrx 0.17 does). That version is in Cargo.lock already, but only
# for an optional feature of aws-lc-sys, so the filter below would replace it
# with a stub. Vendor it fully:
mkdir -p "$WORKDIR/bindgen-0.72/src"
touch "$WORKDIR/bindgen-0.72/src/lib.rs"
cat > "$WORKDIR/bindgen-0.72/Cargo.toml" <<'CARGOEOF'
[package]
name = "bindgen-0-72"
version = "0.0.0"
edition = "2021"

[dependencies]
bindgen = { version = "=0.72.1", default-features = false, features = ["experimental", "runtime"] }
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
	--sync="$WORKDIR/bindgen-0.72/Cargo.toml" \
	--all-features --keep-dep-kinds=no-dev vendor
tar --sort=name --mtime=@0 --owner=0 --group=0 --numeric-owner -cf - Cargo.lock vendor | xz -T0 -6 > "$WORKDIR/pg_parquet-$VERSION-vendor.tar.xz"
xz -t "$WORKDIR/pg_parquet-$VERSION-vendor.tar.xz"

mv "$WORKDIR/pg_parquet-$VERSION-vendor.tar.xz" "$TOPDIR/"
cd "$TOPDIR"
rm -rf "$TOPDIR/tmp"
