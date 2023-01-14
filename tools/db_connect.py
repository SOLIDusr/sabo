import psycopg2 as sql
from tools.logs import Log as logger
from configs.database_config import *


def init():

    global cursor
    try:
        data_base = sql.connect(
                host=host,
                user=user,
                password=password,
                database=db_name,
                port=port,
            )
        data_base.autocommit = True

        cursor = data_base.cursor()
        logger.info('Database connected')

    except (Exception, sql.Error) as _er:

        logger.fatal(f'Failed to connect to PostgreSQL! Error:\n {_er}')
        exit(-1)

init()