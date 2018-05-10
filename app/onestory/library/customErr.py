class CustomErr(Exception):

    success_code = 10000
    common_err_code = 10001
    obj_err_code = 11001
    user_not_find_err = 10002

    def __init__(self, err_code, err_msg):
        super().__init__(self)
        self.error_info = err_msg
        self.error_code = err_code

    def __str__(self):
        return self.error_info

