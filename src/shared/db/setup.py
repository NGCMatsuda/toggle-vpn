import pymysql

from shared.db.helpers import parse_database_credentials


def __create_database(db_username, db_password, db_host, db_name):
    connection = pymysql.connect(
        host=db_host,
        user=db_username,
        password=db_password,
        db='mysql',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor)

    try:
        with connection.cursor() as cursor:
            cursor.execute(f'CREATE DATABASE IF NOT EXISTS {db_name} COLLATE utf8mb4_ja_0900_as_cs');

        connection.commit()
    finally:
        connection.close()


def setup_database(database_uri):
    db_username, db_password, db_host, db_name = parse_database_credentials(database_uri)

    if db_username and db_password and db_host and db_name:
        __create_database(db_username, db_password, db_host, db_name)
