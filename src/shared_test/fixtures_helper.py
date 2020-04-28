import os


def truncate_database(db_engine, session):
    drop_tables = db_engine.execute(
        f"""SELECT CONCAT('DROP TABLE `', TABLE_SCHEMA, '`.`', TABLE_NAME, '`;')
        FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = '{db_engine.url.database}'""")

    drop_routines = db_engine.execute(
        f"""SELECT
        CONCAT('DROP ', ROUTINE_TYPE, ' `', ROUTINE_SCHEMA, '`.`', ROUTINE_NAME, '`;')
        FROM information_schema.ROUTINES WHERE ROUTINE_SCHEMA = '{db_engine.url.database}'""")

    cleanup = ['SET FOREIGN_KEY_CHECKS = 0;']
    cleanup.extend([drop_table[0] for drop_table in drop_tables])
    cleanup.extend([drop_routine[0] for drop_routine in drop_routines])
    cleanup.extend(['SET FOREIGN_KEY_CHECKS = 1;'])

    [session().execute(query, bind=db_engine) for query in cleanup]


def load_database_schema(db_engine, session, sql_path='db/schema.sql'):
    if not sql_path or not os.path.exists(sql_path):
        sql_path = __autodetect_sql_schema_path()

    if not sql_path:
        raise Exception('Could not locate SQL schema file')

    with open(sql_path, 'r') as file:
        lines = file.read().split(';')
        queries = [line for line in lines if line.strip()]
        for query in queries:
            session().execute(query, bind=db_engine)


def __autodetect_sql_schema_path():
    for path in os.getenv('PYTHONPATH').split(os.pathsep):
        sql_path = f'{path}/db/schema.sql'
        if os.path.isfile(sql_path):
            return sql_path
