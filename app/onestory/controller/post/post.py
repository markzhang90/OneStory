#!/usr/bin/python
# -*- coding: UTF-8 -*-
from app.onestory.controller.base import base
import app.onestory.library.common as comm
import app.onestory.library.customErr as customErr
from app.onestory.service.models.post import posts
from app.onestory.service.models.user import user

import time, random


class AddPostHandler(base.BaseHandler):

    def get(self, *args, **kwargs):
        self.required_user_login()
        arg_list = {
            'id': 0,
            'storyid': -1,
            'header': '无题',
            'rel': '',
            'content': '今天什么都没有留下',
            'ext': ''
        }
        self.must_get_args_check(arg_list)
        my_args = self.get_vars
        passid = my_args["_passid"]
        user_service = user.UserOperation()
        user_info = user.UserInfo(passid=passid)
        get_user = user_service.try_get_user_by_cache(user_info)
        post_data = posts.PostInfo(
            story_id=None,
            uid=None,
            passid=None,
            header=None,
            rel=None,
            content=None,
            create_date=1,
            update_time=None,
            ext=None
        )

class GetPostInfoHandler(base.BaseHandler):

    @comm.decorator
    def get(self, *args, **kwargs):
        arg_list = {
            'passid': 0,
            'storyid': -1,
            'starttime': -1,
            'endtime': -1,
            'orderby': 'desc',
            'page': 1,
            'limit': 10,
        }
        post_list = []
        post_res = {}
        try:
            self.must_get_args_check(arg_list)
            my_args = self.get_vars
            if my_args['orderby'] != "desc":
                my_args['orderby'] = "asc"
            posts_op = posts.PostOperation()
            get_res = posts_op.get_posts_list(
                passid=my_args['passid'],
                storyid=my_args['storyid'],
                time_start=int(my_args['starttime']),
                time_end=int(my_args['endtime']),
                page=int(my_args['page']),
                limit=int(my_args['limit']),
                orderby= my_args['orderby']
            )
            get_res_count = posts_op.get_posts_list_count(
                passid=my_args['passid'],
                storyid=my_args['storyid'],
                time_start=int(my_args['starttime']),
                time_end=int(my_args['endtime']),
            )
            for each_post in get_res:
                if isinstance(each_post, posts.PostInfo):
                    post_list.append(each_post.get_post())
            post_res['list'] = post_list
            post_res['page'] = my_args['page']
            post_res['limit'] = my_args['limit']
            post_res['count'] = get_res_count
            return self.finish_out(customErr.CustomErr.success_code, 'success', post_res)
        except customErr.CustomErr as e:
            return self.finish_out(e.error_code, e.error_info, post_res)


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
