#!/usr/bin/bash

#################################################
#						#
# Devrim Gündüz <devrim@gunduz.org> - 2024	#
#						#
#################################################

source ~/bin/global.sh

~/bin/s3indexbuilder.py $awssrpmurl srpms/ --cfdistribution $CF_SRPM_DISTRO_ID
~/bin/s3indexbuilder.py $awsdebuginfourl debug/ --cfdistribution $CF_DEBUG_DISTRO_ID

# Invalidate the CloudFront caches of everything the builders synced. The sync
# scripts do not, unless a specific PostgreSQL version was passed to them. One
# wildcard path per distribution, as CloudFront allows only 15 wildcard paths
# in progress per distribution. Without the "*", only the /srpms and /debug
# objects themselves would be invalidated:
aws cloudfront create-invalidation --distribution-id "$CF_SRPM_DISTRO_ID" --paths '/srpms/*'
aws cloudfront create-invalidation --distribution-id "$CF_DEBUG_DISTRO_ID" --paths '/debug/*'
