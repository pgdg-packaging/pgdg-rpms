#!/usr/bin/bash

#########################################################
#							#
# Devrim Gündüz <devrim@gunduz.org> - 2024		#
#							#
#########################################################

# Include common values:
source ~/bin/global.sh

# Make sure only postgres user can run this script:
if [ "$(id -u)" != "26" ]; then
	clear
	echo
	echo "${red}ERROR:${reset} This script must be run as postgres user" 1>&2
	echo
	exit 1
fi

# First clean common directory:
rm -rf ~/rpmcommon/BUILD/*
rm -rf ~/rpmcommon/BUILDROOT/*

rm -rf /var/lib/pgsql/rpm${pgAlphaVersion}testing/BUILD/*
rm -rf /var/lib/pgsql/rpm${pgAlphaVersion}testing/BUILDROOT/*

# Now clean testing dirs:
for packageCleanVersion in ${pgTestBuilds[@]}
do
	rm -rf /var/lib/pgsql/rpm${packageCleanVersion}testing/BUILD/*
	rm -rf /var/lib/pgsql/rpm${packageCleanVersion}testing/BUILDROOT/*
done

# Clean up extras build directory:
if [ $extrasrepoenabled = 1 ]
then
	rm -rf /var/lib/pgsql/pgdg.$osshort.extras/BUILD/*
	rm -rf /var/lib/pgsql/pgdg.$osshort.extras/BUILDROOT/*
fi

# Finally, delete stable dirs:
for packageCleanVersion in ${pgStableBuilds[@]}
do
	rm -rf /var/lib/pgsql/rpm${packageCleanVersion}/BUILD/*
	rm -rf /var/lib/pgsql/rpm${packageCleanVersion}/BUILDROOT/*
done

