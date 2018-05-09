#!/usr/bin/python
# -*- coding: UTF-8 -*-
from app.onestory.controller.base import base
import app.onestory.library.common as comm
import app.onestory.library.customErr as customErr
from app.onestory.service.models.user import user
import time, random


class GetPostInfoHandler(base.BaseHandler):

    @comm.decorator
    def get(self, *args, **kwargs):
        arg_list = {
            'openid': 0,
            'passid': 0,
        }
        try:
            self.must_get_args_check(arg_list)
            my_args = self.get_vars
            if my_args['passid'] == 0 and my_args['openid'] == 0:
                raise customErr.CustomErr(customErr.CustomErr.common_err_code, 'params missing')
            user_info = user.UserOperation.get_user_info(my_args['passid'], my_args['openid'])
            return self.finish_out(customErr.CustomErr.success_code, 'success', user_info.get_clean_user_info())
        except customErr.CustomErr as e:
            return self.finish_out(e.error_code, e.error_info, {})


class InsertNewPostHandler(base.BaseHandler):

    @comm.decorator
    def get(self, *args, **kwargs):
        load_time = int(time.time())
        arg_list = {
            'nick_name': None,
            'password': None,
            'email': None,
            'phone': None,
            'openid': 0,
            'avatar': None,
            'ext': '',
            'update_time': load_time,
            'active': 1,
        }

        try:
            self.must_get_args_check(arg_list)
        except customErr.CustomErr as e:
            return self.finish_out(e.error_code, e.error_info, {})

        except ValueError as e_val:
            return self.finish_out(10001, 'value error', {})

        my_args = self.get_vars
        my_args['passid'] = str(load_time * 10000 + random.randint(1, 9999))
        my_args['password'] = user.UserInfo.encode_password(my_args['password'])
        user_info = user.UserInfo(
            nick_name=my_args['nick_name'],
            password=my_args['password'],
            email=my_args['email'],
            phone=my_args['phone'],
            openid=my_args['openid'],
            passid=my_args['passid'],
            avatar=my_args['avatar'],
            ext=my_args['ext'],
            update_time=my_args['update_time'],
            active=my_args['active'],
        )

        try:
            userop = user.UserOperation()
            res = userop.insert_alchemy_user(user_info)
        except Exception as e:
            print(e)
            res = False
        if not res:
            return self.finish_out(customErr.CustomErr.common_err_code, 'insert user fail', res)

        return self.finish_out(10000, 'success', user_info.get_all_user())
