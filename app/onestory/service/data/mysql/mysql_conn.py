import pymysql.cursors
import app.onestory.conf.config as config
from contextlib import contextmanager


class MySql(object):
    __first_init = True

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(MySql, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        if self.__first_init:
            self.connection = {}
            self.__first_init = False

    def get_connection(self, dbname="onestory"):
        if dbname not in self.connection:
            db_host = config.load_config("db", "db_host")
            db_port = config.load_config("db", "db_port")
            db_user = config.load_config("db", "db_user")
            db_pass = config.load_config("db", "db_pass")
            connection = pymysql.connect(host=db_host,
                                         port=int(db_port),
                                         user=db_user,
                                         password=db_pass,
                                         db=dbname,
                                         charset='utf8mb4',
                                         cursorclass=pymysql.cursors.DictCursor)
            connection.autocommit(1)
            self.connection[dbname] = connection
        return self.connection[dbname]

    @contextmanager
    def get_cursor(self, dbname="onestory"):
        current_conn = self.get_connection(dbname)
        cursor = current_conn.cursor()
        try:
            yield cursor
        finally:
            cursor.close()

    def done_and_close(self, dbname="onestory"):
        current_conn = self.connection.pop(dbname)
        current_conn.close()

    def query(self, query, data):
        with self.get_cursor() as cursor:
            return cursor.execute(query, data)


