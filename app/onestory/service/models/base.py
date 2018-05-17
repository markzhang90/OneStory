from app.onestory.service.data.mysql import alchemyConn
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class OperationBase(object):

    session = None

    def __init__(self, Session):
        if self.session is None:
            self.session = Session()

    def load_session(self):
        mysqlConn = alchemyConn.MysqlConn()
        Session = mysqlConn.get_session()
        self.session = Session()

    def __del__(self):
        if self.session is not None:
            # self.session.close()
            # self.session = None
            pass

    def close_session(self):
        if self.session is not None:
            print("close session")
            self.session.close()
            self.session = None

    def insert_new_obj(self, new_object):
        if self.session is None:
            self.load_session()
        self.session.add(new_object)
        try:
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e
        return new_object
