#!/bin/bash

echo "START Backup single DB"

# stop on errors
set -e

# check that we have right number of arguments
if [[ ! $# -eq 2 ]]
then
    echo 'usage:'
    echo '    /pgbackup/backup.sh <container_name> <backup-file>'
    echo ''
    echo 'to get a list of available backups, run:'
    echo '    /pgbackup/list-backups.sh'
    exit 1
fi

# set the container name variable
CONTAINERNAME=$1

# set the backupfile variable
BACKUPFILE=$2

echo "Backing up ${CONTAINERNAME} to ${BACKUPFILE}"

pushd /pgbackup
	python3 pgbackup.py --filepath ${BACKUPFILE} --containername ${CONTAINERNAME} backup
popd

echo "END Backup"
