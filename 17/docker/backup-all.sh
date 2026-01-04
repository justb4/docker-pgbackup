#!/bin/bash

echo "START Backup"

pushd /pgbackup
	python3 pgbackup.py --backupdir /backup backup-all
popd

echo "END Backup"
