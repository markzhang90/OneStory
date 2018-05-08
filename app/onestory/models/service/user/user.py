#! /usr/bin/env python
# -*- coding:utf-8 -*-

from app.onestory.models.data.mysql import conn
import app.onestory.library.customErr as customErr

import hashlib


class UserOperation(object):

    def __init__(self):
        pass

    @classmethod
    def insert_new_user(cls, user_info):

        if not isinstance(user_info, UserInfo):
            raise customErr.CustomErr(customErr.CustomErr.obj_err_code, 'user_info object failure')
        new_conn = conn.MySql()
        sql = 'INSERT INTO user_profile (openid, passid, email, phone, password, update_time, nick_name, avatar, ' \
              'ext, active) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        data = (user_info.openid, user_info.passid, user_info.email, user_info.phone, user_info.password, user_info.update_time, user_info.nick_name, user_info.avatar,
                user_info.ext, user_info.active)

        with new_conn.get_cursor() as cursor:
            try:
                res = cursor.execute(sql, data)
                if res != 1:
                    raise customErr.CustomErr(customErr.CustomErr.common_err_code, 'insert fail')
            except Exception as e:
                res = False
        new_conn.done_and_close()
        return res

    @classmethod
    def get_user_info(cls, pass_id=None, open_id=None):
        if pass_id is None and open_id is None:
            raise customErr.CustomErr(customErr.CustomErr.obj_err_code, 'user identify get failure')

        if open_id is not None and open_id != 0:
            op = 'openid'
            val = open_id
        else:
            op = 'passid'
            val = pass_id

        new_conn = conn.MySql()
        sql = 'SELECT * FROM user_profile where ' + op + ' = %s'
        data = (val,)

        user_info = None
        with new_conn.get_cursor() as cursor:
            try:
                res = cursor.execute(sql, data)
                if res != 1:
                    raise customErr.CustomErr(customErr.CustomErr.common_err_code, 'get user fail')
                result = cursor.fetchone()
                user_info = UserInfo(result)
            except Exception as e:
                pass
        new_conn.done_and_close()

        return user_info


class UserInfo(object):

    def __init__(self, user_obj={}):
        self.id = user_obj['id'] if 'id' in user_obj else None
        self.openid = user_obj['openid'] if 'openid' in user_obj else None
        self.passid = user_obj['passid'] if 'passid' in user_obj else None
        self.email = user_obj['email'] if 'email' in user_obj else None
        self.phone = user_obj['phone'] if 'phone' in user_obj else 0
        self.password = user_obj['password'] if 'password' in user_obj else None
        self.update_time = user_obj['update_time'] if 'update_time' in user_obj else None
        self.nick_name = user_obj['nick_name'] if 'nick_name' in user_obj else None
        self.avatar = user_obj['avatar'] if 'avatar' in user_obj else None
        self.ext = user_obj['ext'] if 'ext' in user_obj else ''
        self.active = user_obj['active'] if 'active' in user_obj else 1

    @staticmethod
    def encode_password(password):
        hl = hashlib.md5()
        hl.update(password.encode(encoding='utf-8'))
        encoded = hl.hexdigest()
        return encoded

    @staticmethod
    def encode_passid(pass_id):
        hl = hashlib.md5()
        hl.update(pass_id.encode(encoding='utf-8'))
        encoded = hl.hexdigest()
        return encoded

    def get_clean_user_info(self):
        return {
            'nick_name': self.nick_name,
            'openid': self.openid,
            'passid': self.passid,
            'avatar': self.avatar,
            'update_time': self.update_time,
            'ext': self.ext,
            'active': self.active,
        }

    def get_all_user(self):
        return {
            'id': self.id,
            'nick_name': self.nick_name,
            'openid': self.openid,
            'passid': self.passid,
            'email': self.email,
            'phone': self.phone,
            'password': self.password,
            'avatar': self.avatar,
            'update_time': self.update_time,
            'ext': self.ext,
            'active': self.active,
        }