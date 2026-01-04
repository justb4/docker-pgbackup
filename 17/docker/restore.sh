#!/bin/bash

echo "START Restore"

# stop on errors
set -e

# check that we have right number of arguments
if [[ ! $# -eq 2 ]]
then
    echo 'usage:'
    echo '    /pgbackup/restore.sh <container_name> <backup-file>'
    echo ''
    echo 'to get a list of available backups, run:'
    echo '    /pgbackup/list-backups.sh'
    exit 1
fi

# set the container name variable
CONTAINERNAME=$1

# set the backupfile variable
BACKUPFILE=$2

# check that the file exists
if [ ! -f ${BACKUPFILE} ]
then
    echo "backup file not found"
    echo 'to get a list of available backups, run:'
    echo '    /pgbackup/list-backups.sh'
    exit 1
fi


echo "Restoring to ${CONTAINERNAME} from ${BACKUPFILE}"

pushd /pgbackup
	python3 pgbackup.py --filepath ${BACKUPFILE} --containername ${CONTAINERNAME} restore
popd

echo "END Restore"
