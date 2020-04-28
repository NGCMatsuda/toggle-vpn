import os

from shared.db.helpers import parse_database_credentials


def dump_schema(database_uri, target='db/schema.sql'):
    db_username, db_password, db_host, db_name = parse_database_credentials(database_uri)
    os.system(f'docker exec `docker-compose ps -q mysql` mysqldump -u{db_username} -p{db_password} --no-data ' +
              f'--skip-comments {db_name} | grep -v "^mysqldump:.*$" | sed "s/ AUTO_INCREMENT=[0-9]*//g" > {target}')

    os.system(f'docker exec `docker-compose ps -q mysql` mysqldump -u{db_username} -p{db_password} ' +
              f'--skip-comments --no-create-info {db_name} migrate_version | grep -v "^mysqldump:.*$" >> {target}')
