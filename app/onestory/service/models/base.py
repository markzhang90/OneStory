from app.onestory.service.data.mysql import alchemyConn
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class OperationBase(object):

    session = None

    def __init__(self):
        if self.session is None:
            self.load_session()

    def load_session(self):
        mysqlConn = alchemyConn.MysqlConn()
        Session = mysqlConn.get_session()
        self.session = Session()

    def __del__(self):
        if self.session is not None:
            self.session.close()
            self.session = None

    def insert_alchemy(self, new_object):
        if self.session is None:
            self.load_session()
        self.session.add(new_object)
        self.session.commit()
        return True