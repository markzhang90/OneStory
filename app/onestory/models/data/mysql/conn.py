import pymysql.cursors
import app.onestory.conf.config as config


class MySql(object):
    __first_init = True

    def __new__(cls):
        print("in new")
        print(cls)
        if not hasattr(cls, 'instance'):
            cls.instance = super(MySql, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        if self.__first_init:
            self.connection = {}
            self.__first_init = False

    def get_connection(self, dbname="onestory"):
        if dbname not in self.connection:
            print(111)
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
            self.connection[dbname] = connection
        return self.connection[dbname]
