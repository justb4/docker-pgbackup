#!/bin/bash

PGB_SCHEDULE=${PGB_SCHEDULE:='0 23 * * *'}

pushd /pgbackup

envsubst < cronfile-template  > backup-cron

# Now launch cron in then foreground.
echo "Launching /usr/sbin/crond in foregound with schedule:"
cat backup-cron
crontab backup-cron
/usr/sbin/crond -f -S -l 0
