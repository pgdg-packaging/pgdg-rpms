#!/usr/bin/bash

#########################################################
#							#
# Devrim Gündüz <devrim@gunduz.org> - 2024		#
#							#
#########################################################

# Include common values:
source ~/bin/global.sh

# Check eack PostgreSQL major release:

for packageBuildVersion in ${pgStableBuilds[@]}
do
	echo "Checking PostgreSQL $packageBuildVersion - $os"
	upload_status=`curl -s -o /dev/null -w "%{http_code}" https://download.postgresql.org/pub/repos/yum/$packageBuildVersion/$osdistro/$os-$osarch/repodata/`
	echo "Status: $upload_status"
	if [ $upload_status == "404" ]
	then
		echo "${red}ERROR:${reset} There is a problem with the PostgreSQL $packageBuildVersion status"
	fi
	echo
done

# Also check the common repo:

echo "Checking $os common repo:"
upload_status=`curl -s -o /dev/null -w "%{http_code}" https://download.postgresql.org/pub/repos/yum/common/$osdistro/$os-$osarch/repodata/`
echo "Status: $upload_status"
if [ $upload_status == "404" ]
then
	echo "${red}ERROR:${reset} There is a problem with the $os common repo"
fi
echo

exit 0
