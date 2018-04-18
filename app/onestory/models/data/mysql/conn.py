import pymysql.cursors
import app.onestory.conf.config as config


class MySql(object):

    def __init__(self):
        db_host = config.load_config("db", "db_host")
        db_port = config.load_config("db", "db_port")
        db_user = config.load_config("db", "db_user")
        db_pass = config.load_config("db", "db_pass")
        self.connection = pymysql.connect(host=db_host,
                                          port=int(db_port),
                                          user=db_user,
                                          password=db_pass,
                                          db='onestory',
                                          charset='utf8mb4',
                                          cursorclass=pymysql.cursors.DictCursor)

    def get_connection(self):
        return self.connection

