#!/usr/bin/bash

set -euo pipefail

if [ $# -lt 1 ]; then
	echo "Usage: $0 version"
	exit 1
fi

VERSION="$1"
TOPDIR="$PWD"
WORKDIR="$TOPDIR/tmp/pgvectorscale-$VERSION"

mkdir -p "$WORKDIR" && cd "$WORKDIR"
curl -Lo pgvectorscale-$VERSION.tar.gz https://github.com/timescale/pgvectorscale/archive/refs/tags/$VERSION.tar.gz
tar xf pgvectorscale-$VERSION.tar.gz
cd pgvectorscale-$VERSION/
# Keep the crate cache and the temporary files out of the source tree and /tmp:
export CARGO_HOME="$WORKDIR/cargo-home" TMPDIR="$WORKDIR/tmp"
mkdir -p "$TMPDIR"
# Upstream does not ship a Cargo.lock, so create one. It is shipped in the
# tarball next to the vendor directory, so that the build uses exactly the
# crates that were vendored:
cargo generate-lockfile
# pgrx-bindgen 0.16.1 needs bindgen 0.71, which creates opaque structs from the
# PostgreSQL headers with newer clang versions. The spec switches it to bindgen
# 0.72.1 (as pgrx 0.17 does), so vendor that version too:
mkdir -p "$WORKDIR/bindgen-0.72/src"
touch "$WORKDIR/bindgen-0.72/src/lib.rs"
cat > "$WORKDIR/bindgen-0.72/Cargo.toml" <<'EOF'
[package]
name = "bindgen-0-72"
version = "0.0.0"
edition = "2021"

[dependencies]
bindgen = { version = "=0.72.1", default-features = false, features = ["experimental", "runtime"] }
EOF
# Only keep the crates for the Linux architectures that we build on. The other
# crates are replaced with empty stubs, so that Cargo.lock still resolves. Needs
# cargo-vendor-filterer. ('*-unknown-linux-gnu' does not work, as the LLVM of
# Fedora cannot create a target machine for m68k.) The dev dependencies are kept:
# --keep-dep-kinds=no-dev fails with "Invalid output received from cargo tree",
# as cargo tree prints an empty line between the two workspace members.
cargo vendor-filterer \
	--platform=x86_64-unknown-linux-gnu \
	--platform=aarch64-unknown-linux-gnu \
	--platform=powerpc64le-unknown-linux-gnu \
	--platform=s390x-unknown-linux-gnu \
	--sync="$WORKDIR/bindgen-0.72/Cargo.toml" \
	--all-features vendor
tar --sort=name --mtime=@0 --owner=0 --group=0 --numeric-owner -cf - Cargo.lock vendor | xz -T0 -6 > "$WORKDIR/pgvectorscale-$VERSION-vendor.tar.xz"
xz -t "$WORKDIR/pgvectorscale-$VERSION-vendor.tar.xz"

mv "$WORKDIR/pgvectorscale-$VERSION-vendor.tar.xz" "$TOPDIR/"
cd "$TOPDIR"
rm -rf "$TOPDIR/tmp"
