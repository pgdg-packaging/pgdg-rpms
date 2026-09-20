#!/usr/bin/bash

#########################################################
#							#
# Devrim Gündüz <devrim@gunduz.org> - 2026		#
#							#
#########################################################

# Include common values:
source ~/bin/global.sh

# Sign all packages across all repo directories.
# sign_package() filters by $signPackageName and $packageVersion; setting
# both to "*" ensures every RPM in each directory tree is matched.
signPackageName="*"
packageVersion="*"

overall_status=0

for rpm_dir_prefix in rpmcommon pgdg rpm1 rpm2; do
	# Only attempt signing if at least one matching directory exists:
	if compgen -G ~/"${rpm_dir_prefix}"* > /dev/null 2>&1; then
		sign_package "${rpm_dir_prefix}" || overall_status=1
	fi
done

exit $overall_status
