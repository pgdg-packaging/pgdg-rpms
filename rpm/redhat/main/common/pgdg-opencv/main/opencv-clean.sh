#!/bin/bash
# Repack the OpenCV source tarball without the "Lena" image, whose
# redistribution terms are unclear, as the Fedora package does.
# usage: opencv-clean.sh <version>   (in this directory)
set -e
VERSION=$1
[ -f opencv-${VERSION}.tar.gz ] || curl -sfL -o opencv-${VERSION}.tar.gz https://github.com/opencv/opencv/archive/${VERSION}/opencv-${VERSION}.tar.gz
W=$(mktemp -d)
tar xf opencv-${VERSION}.tar.gz -C $W
find $W/opencv-${VERSION}/ \( -iname "*lena*" -o -iname "*lenna*" \) -exec rm {} ';' -print
tar -C $W -zcf opencv-clean-${VERSION}.tar.gz opencv-${VERSION}/
rm -rf $W opencv-${VERSION}.tar.gz
