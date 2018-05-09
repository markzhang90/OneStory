#! /usr/bin/env python
# -*- coding:utf-8 -*-

import hashlib

from sqlalchemy import Column, Integer, String, TEXT
from sqlalchemy.ext.declarative import declarative_base

import app.onestory.library.customErr as customErr
from app.onestory.service.data.mysql import conn
from app.onestory.service.models.base import OperationBase

Base = declarative_base()


class UserOperation(OperationBase):

    def insert_alchemy_user(self, user_info):
        if self.session is None:
            self.load_session()
        self.session.add(user_info)
        try:
            self.session.commit(user_info)
        except Exception as e:
            self.session.rollback()
            raise e
        return True

    def query_user_info(self, user_info):
        if self.session is None:
            self.load_session()
        if user_info.passid is None and user_info.openid is None:
            raise customErr.CustomErr(customErr.CustomErr.obj_err_code, 'user identify get failure')
        try:
            if user_info.openid is not None and user_info.openid != 0:
                res_user = self.session.query(UserInfo).filter_by(openid=user_info.openid).one()
            else:
                res_user = self.session.query(UserInfo).filter_by(passid=user_info.passid).one()
        except Exception as e:
            self.session.rollback()
            raise e
        return res_user


    @classmethod
    def insert_new_user(cls, user_info):

        if not isinstance(user_info, UserInfo):
            raise customErr.CustomErr(customErr.CustomErr.obj_err_code, 'user_info object failure')
        new_conn = conn.MySql()
        sql = 'INSERT INTO user_profile (openid, passid, email, phone, password, update_time, nick_name, avatar, ' \
              'ext, active) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        data = (
            user_info.openid, user_info.passid, user_info.email, user_info.phone, user_info.password,
            user_info.update_time,
            user_info.nick_name, user_info.avatar,
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


class UserInfo(Base):
    __tablename__ = 'user_profile'
    id = Column(Integer, primary_key=True)
    nick_name = Column(String(10), nullable=False)
    openid = Column(String(64), nullable=False, unique=True)
    passid = Column(String(64), nullable=False, unique=True)
    email = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    avatar = Column(String(255), nullable=False)
    active = Column(Integer, nullable=False)
    ext = Column(TEXT, nullable=False)
    phone = Column(Integer, nullable=False)
    update_time = Column(Integer, nullable=False)

    def __init__(self,
                 pid=None,
                 openid=None,
                 passid=None,
                 email=None,
                 phone=None,
                 password=None,
                 update_time=0,
                 nick_name=None,
                 avatar=None,
                 ext=None,
                 active=1):
        self.id = pid
        self.openid = openid
        self.passid = passid
        self.email = email
        self.phone = phone
        self.password = password
        self.update_time = update_time
        self.nick_name = nick_name
        self.avatar = avatar
        self.ext = ext
        self.active = active

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
