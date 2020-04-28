from sqlalchemy import create_engine

from shared.timezone import TZ


def create_engine_with_timezone_and_charset(db_url, tz=TZ, charset='utf8mb4'):
    return create_engine(db_url,
                         connect_args=dict(init_command=f'SET @@session.time_zone = "{tz}";', charset=charset),
                         pool_pre_ping=True)
