import time
import click
import docker
import subprocess

client = docker.from_env()
backup_dir = None
container_name = None
file_path = None

def echo(s):
    click.echo(s)

def get_enabled_containers():
    filters = {'label': 'pgbackup.enable=true'}

    containers = client.containers.list(filters=filters)
    return containers

def get_enabled_container(container_name):
    containers = get_enabled_containers()
    found_container = None
    for container in containers:
        if container.name == container_name:
            found_container = container
    return found_container

def get_pg_creds(container):
    pg_creds = dict()
    pg_creds['PGHOST'] = container.name
    pg_creds['PGPORT'] = '5432'

    env_list = container.attrs['Config']['Env']
    for env_kv in env_list:
        # Matches POSTGRES_DB and POSTGRES_DBNAME
        if 'POSTGRES_DB' in env_kv:
            pg_creds['PGDB'] = env_kv.split('=')[1]
        if 'POSTGRES_USER' in env_kv:
            pg_creds['PGUSER'] = env_kv.split('=')[1]
        # Matches POSTGRES_PASS and POSTGRES_PASSWORD
        if 'POSTGRES_PASS' in env_kv:
            pg_creds['PGPASSWORD'] = env_kv.split('=')[1]

    return pg_creds


def make_backup_cmd(pg_creds, file_path):
    cmd_template = 'export PGPASSWORD=%s; pg_dump -h %s -U %s %s | gzip > %s'
    cmd = cmd_template % (
        pg_creds['PGPASSWORD'], pg_creds['PGHOST'],
        pg_creds['PGUSER'], pg_creds['PGDB'],
        file_path)
    return cmd


def make_dropdb_cmd(pg_creds):
    cmd_template = 'export PGPASSWORD=%s; dropdb -h %s -U %s %s'
    cmd = cmd_template % (
        pg_creds['PGPASSWORD'], pg_creds['PGHOST'],
        pg_creds['PGUSER'], pg_creds['PGDB']
    )
    return cmd


def make_createdb_cmd(pg_creds):
    cmd_template = 'export PGPASSWORD=%s; createdb -h %s -U %s -O %s %s'
    cmd = cmd_template % (
        pg_creds['PGPASSWORD'], pg_creds['PGHOST'], pg_creds['PGUSER'],
        pg_creds['PGUSER'], pg_creds['PGDB']
    )
    return cmd


def make_restore_cmd(pg_creds, file_path):
    cmd_template = 'export PGPASSWORD=%s; gunzip -c %s | psql -h %s -U %s %s '
    cmd = cmd_template % (
        pg_creds['PGPASSWORD'], file_path, pg_creds['PGHOST'],
        pg_creds['PGUSER'], pg_creds['PGDB']
        )
    return cmd


def execute_cmd(cmd):
    echo('executing cmd=%s' % cmd)
    exit_code = subprocess.call(cmd, shell=True)
    echo('execute done, exit_code=%d' % exit_code)


@click.group()
@click.option('--backupdir', help='Backup root directory')
@click.option('--containername', required=False, help='Optional container name for backup single or restore')
@click.option('--filepath', required=False, help='Optional backup file for backup single or restore')
def cli(backupdir, containername, filepath):
    global backup_dir
    global container_name
    global file_path
        
    backup_dir = backupdir
    container_name = containername
    file_path = filepath
    echo('backupdir=%s' % backup_dir)


@cli.command()
def backup_all():
    echo('START backup_all')
    containers = get_enabled_containers()
    echo('Found %d containers with backup enabled' % len(containers))
    for container in containers:
        echo('Backing up %s ...' % container.name)
        now = time.localtime()
        pg_creds = get_pg_creds(container)
        echo('creds: %s' % str(pg_creds))

        dir_path = '%s/%s' % (backup_dir, time.strftime("%Y/%m", now))
        file_path = '%s/%s-%s.sql.gz' % (dir_path, container.name, time.strftime("%y%m%d-%H%M", now))

        execute_cmd('mkdir -p %s' % dir_path)

        backup_cmd = make_backup_cmd(pg_creds, file_path)
        echo('backup_cmd=%s' % backup_cmd)
        execute_cmd(backup_cmd)

    echo('END backup_all')


@cli.command()
def backup():
    echo('backup single for container %s' % container_name)
    container = get_enabled_container(container_name)
    pg_creds = get_pg_creds(container)

    backup_cmd = make_backup_cmd(pg_creds, file_path)
    execute_cmd(backup_cmd)


@cli.command()
def restore():
    echo('restore single for container %s' % container_name)

    container = get_enabled_container(container_name)
    pg_creds = get_pg_creds(container)

    # Three steps: drop existing DB, create new DB and restore
    dropdb_cmd = make_dropdb_cmd(pg_creds)
    execute_cmd(dropdb_cmd)

    createdb_cmd = make_createdb_cmd(pg_creds)
    execute_cmd(createdb_cmd)

    restore_cmd = make_restore_cmd(pg_creds, file_path)
    execute_cmd(restore_cmd)


if __name__ == '__main__':
    cli()
