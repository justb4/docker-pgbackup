# Docker PG Backup Test

Inspired by: https://github.com/kartoza/docker-pg-backup

Uses a simple [docker-compose.yml](docker-compose.yml) to start a PostGIS DB
plus a `pgbackup` container.

## Running

Invoke [start.sh](start.sh). Optionally look at logs:

```
docker logs --follow pg_backup_client
```

As the backup runs every minute, it could be that the `pg_backup_db` container is not yet
up completely thus PG DB not ready.

Invoke [stop.sh](stop.sh) to stop.  Look under `./backup` for backup files.

## TIP - explicit backup

Simply `bash` into `pgbackup` container.

```
	$ docker exec -it pg_backup_client bash
	$ /backup.sh
```

## TIP - explicit restore

Copy `<your_backup_file>.sql.gz` into the `./backup` directory.
Simply `bash` into `pgbackup` container.

```
	$ docker exec -it pg_backup_client bash
	$ /restore.sh /backup/<your_backup_file>.sql.gz
```

## TIP - connect with psql

Simply `bash` into `pgbackup` container, using the env settings file.

```
	$ docker exec -it pg_backup_client bash
	$ source /pgb-env.sh
	$ psql <no args required>
```

