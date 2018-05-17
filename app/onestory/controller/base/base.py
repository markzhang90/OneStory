import tornado.web
import app.onestory.library.common as comm
import app.onestory.library.customErr as customErr
from app.onestory.service.data.mysql import alchemyConn
from concurrent.futures import ThreadPoolExecutor

class BaseHandler(tornado.web.RequestHandler):

    cookie_expire_days = 3
    __get_vars = {}
    Session = None
    executor = ThreadPoolExecutor(10)

    def initialize(self):
        pass

    def prepare(self):
        print("start init")
        mysqlConn = alchemyConn.MysqlConn()
        Session = mysqlConn.get_session()
        self.Session = Session

    def on_finish(self):
        self.__get_vars = {}
        self.Session.remove()
        print("finish")
        print(self.Session)

    def finish_out(self, code, msg, out_arr={}):
        output = {
            'code': code,
            'message': msg,
            'data': out_arr,
        }
        self.set_status(200)
        self.write(comm.json_out(output))
        self.finish()
        return

    def must_get_args_check(self, arg_list):

        for key, val in arg_list.items():
            find_var = self.get_argument(key, None)
            if val is None:
                if find_var is None:
                    raise customErr.CustomErr(20001, "must have " + key + " in request but not find")
                else:
                    self.__get_vars[key] = find_var
            else:
                if find_var is None:
                    self.__get_vars[key] = val
                else:
                    self.__get_vars[key] = find_var
        return self.__get_vars

    def required_user_login(self):
        cookie_pass = self.get_cookie('passid', None)
        if cookie_pass is None:
            self.redirect('login')
        else:
            self.__get_vars['_passid'] = cookie_pass

    @property
    def get_vars(self):
        return self.__get_vars
