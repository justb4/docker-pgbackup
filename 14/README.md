# Docker PG Backup

Inspired by: https://github.com/kartoza/docker-pg-backup

A Docker container that runs automated scheduled PostgreSQL/PostGIS backups for all
PostgreSQL-based Docker Containers in its network that have the Label `"pgbackup.enable=true"`. 

It should work with
the following PostgreSQL/PostGIS Docker images:

* [mdillon/postgis](https://hub.docker.com/r/mdillon/postgis/)
* [Kartoza docker postgis](https://github.com/kartoza//docker-postgis) 
* [Standard PostgreSQL Docker image](https://hub.docker.com/_/postgres/)

Any other PostgreSQL/PostGIS image may work as long as its Container has the `POSTGRES_` environment
variables set (see below).

By default it will create a backup once per night (at 23:00) in a 
nicely ordered directory by container-name/year/month, but you can specify your own schedule.

* Docker hub at: https://registry.hub.docker.com/u/justb4/pgbackup/
* Github at: https://github.com/justb4/docker-pgbackup

## Getting the image

There are various ways to get the image onto your system:

The preferred way (but using most bandwidth for the initial image) is to
get our docker trusted build like this:


```
docker pull justb4/pgbackup:14

```

We highly suggest that you use a tagged image as 
latest may change and may not successfully back up your database. Use the same or 
greater version of postgis as the database you are backing up.
To build the image yourself:

```
docker build -t justb4/pgbackup .
```

If you do not wish to do a local checkout first then build directly from github.

```
git clone git://github.com/justb4/docker-pgbackup
```

## Environment Variables 

* `PGB_SCHEDULE`, crontab schedule line,  if not set, defaults to : `0 23 * * *`

## Run Backups

To create a running container do:

```
docker run --name="pgbackup"\
           -v backup:/backup -v /var/run/docker.sock:/var/run/docker.sock \
           -i -d justb4/pgbackup:14
```
           
In this example a local dir (`./backup`) is mounted inti which the actual backups will be
stored.

Best is to use docker-compose, below the as used
for testing, with a schedule that backs up once a minute.


```
# Test for pgbackup with sample db
version: "3"

services:
  db:
    image: mdillon/postgis:14-alpine
    container_name: pg_db_14
    labels:
      - "pgbackup.enable=true"
    environment:
      - POSTGRES_DB=testdb
      - POSTGRES_USER=testuser
      - POSTGRES_PASSWORD=testpass

  dbbackup:
    image: justb4/pgbackup:14
    container_name: pg_backup_14
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - ./backup:/backup
    environment:
      - PGB_SCHEDULE=*/1 * * * *
  
```

Then run using:

```
docker-compose up -d
```

It is advised to use explicit DB-container-naming, as backups will be stored in
subdirectories (`year/month/<DB-container-name>-ymd-hm.sql.gz`).

## Explicit Backups

You can also run backups (and restores) explicitly, by calling `exec` on the `justb4/pgbackup` 
container, assuming `pgbackup` here.

Backup all DBs containers:

```
docker exec -it pgbackup /pgbackup/backup-all.sh

```

Or you can backup a single DB container:

```
docker exec -it pgbackup /pgbackup/backup.sh <DB container-name> <backup file.sql.gz>


# example
docker exec -it pgbackup /pgbackup/backup.sh pgdb /backup/mybackup.sql.gz

```

## List Backups

You can list all backups available in the container:

```
docker exec -it pgbackup /pgbackup/list-backups.sh

```

## Restoring Backups

This Docker Image also provides restore utilities.

You can `bash` into the `justb4/pgbackup` container and run `restore.sh` or other commands
from there. The following steps are needed:

* if not already present copy your backup file, assuming `/backup/mybackup.sql.gz` here, into the `pgbackup` container mounted volume
* figure out the name of your `justb4/pgbackup` container, assuming `pgbackup` here
* figure out the name of your target DB container, assuming `pgdb` here
* `bash` into the container: `docker exec -it pgbackup /bin/bash`
* execute restore: `/pgbackup/restore.sh /backup/mybackup.sql.gz pgdb`

You could also `exec` directly. Below an example:

```
docker exec -it pgbackup /pgbackup/restore.sh pgdb /backup/2018/10/pgdb-181013-1050.sql.gz

```

## Design and diffs with kartoza/pg-backup

Main difference is that `justb4/pgbackup` uses the Docker API to search within its Docker Network for
Containers that have the Label `"pgbackup.enable=true"`. Using Labels in conjunction with the Docker API
is found in many modern Docker-based services, like e.g. Traefik and Kubernetes.

Each Container to be backed up is then further inspected to get the PostgreSQL credentials
needed to connect with PG tools like `psql`. The Container name will be the PG Hostname 
(TODO: figure out IP address via Docker API,
such that single backup/restores can be run commandline).

This has the following advantages:

* loose coupling, easy to setup
* one `pgbackup` Container can backup multiple PostgreSQL Containers
* no need to configure `pgbackup` with all PG credentials 
 
Further changes:

* works with multiple Docker images for both PostgreSQL and PostGIS (mdillon and kartoza)
* using smaller `postgres:<version>-alpine` as base image (i.s.o. `kartoza/postgis`)
* schedule via env var `PGB_SCHEDULE`
* dumps in SQL gzip format (more portable among PG versions) but may become option in futre
* includes restore command to restore backup file in a named container

## Credits

* Tim Sutton (tim@kartoza.com) for https://github.com/kartoza/docker-pg-backup - Consulted Oct 2018
* Just van den Broecke (https://justobjects.nl) - this version - 2018
