import re


def parse_database_credentials(database_uri):
    match = re.match(re.compile('mysql\+pymysql://([^:]+):([^@]+)@([^/]+)/([^?]+)'), database_uri)
    return match.groups() if match else (None, None, None, None)
