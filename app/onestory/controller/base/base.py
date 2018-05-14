import tornado.web
import app.onestory.library.common as comm
import app.onestory.library.customErr as customErr


class BaseHandler(tornado.web.RequestHandler):

    __get_vars = {}

    def initialize(self):
        pass

    def on_finish(self):
        self.__get_vars = {}

    def finish_out(self, code, msg, out_arr):
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

        self.__get_vars = {}
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
