import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
import app.onestory.conf.config as config


class MysqlConn(object):
    __first_init = True
    __pool_size = 10

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(MysqlConn, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        if self.__first_init:
            self.engines = {}
            self.__first_init = False
        pass

    def get_session(self, dbname="onestory"):

        if dbname not in self.engines:
            db_host = config.load_config("db", "db_host")
            db_port = config.load_config("db", "db_port")
            db_user = config.load_config("db", "db_user")
            db_pass = config.load_config("db", "db_pass")
            engine_template = "mysql+pymysql://%s:%s@%s:%s/%s?charset=utf8" % (db_user, db_pass, db_host, db_port, dbname)
            ENGINE = create_engine(engine_template, max_overflow=20, pool_size=20, echo_pool=True)
            self.engines[dbname] = ENGINE

        _DBSession = sessionmaker(bind=self.engines[dbname])
        return _DBSession


