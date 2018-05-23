#!/usr/bin/python
# -*- coding: UTF-8 -*-
from app.onestory.controller.base import base
import app.onestory.library.common as comm
import app.onestory.library.customErr as customErr
from app.onestory.service.models.post import posts
from app.onestory.service.models.user import user
import time
import threading
from tornado import gen
from tornado import web
from tornado.concurrent import run_on_executor


class AddPostHandler(base.BaseHandler):

    @comm.decorator
    @web.asynchronous
    @gen.coroutine
    def get(self, *args, **kwargs):
        self.required_user_login()
        arg_list = {
            'id': 0,
            'storyid': 0,
            'header': '无题',
            'rel': '',
            'content': '今天什么都没有留下',
            'ext': ''
        }
        self.must_get_args_check(arg_list)
        my_args = self.get_vars
        passid = my_args["_passid"]
        get_user = yield self.get_user_info(passid)
        if get_user is None or not isinstance(get_user, user.UserInfo):
            return self.finish_out(customErr.CustomErr.common_err_code, 'get user fail')
        post_data = posts.PostInfo(
            story_id=my_args["storyid"],
            uid=get_user.id,
            passid=get_user.passid,
            header=my_args["header"],
            rel=my_args["rel"],
            content=my_args["content"],
            create_date=int(time.strftime("%Y%m%d", time.localtime())),
            update_time=int(time.time()),
            ext=my_args["ext"]
        )
        try:
            res = yield self.insert_post(post_data)
        except Exception as e:
            return self.finish_out(customErr.CustomErr.common_err_code, e.__str__())
        return self.finish_out(customErr.CustomErr.success_code, 'success', post_data.get_post())

    @run_on_executor #open thread to work
    def get_user_info(self, passid):
        user_service = user.UserOperation(self.Session)
        user_info = user.UserInfo(passid=passid)
        return user_service.try_get_user_by_cache(user_info)

    @run_on_executor
    def insert_post(self, post_data):
        post_op = posts.PostOperation(self.Session)
        return post_op.insert_new_obj(post_data)


class GetPostInfoById(base.BaseHandler):

    @comm.decorator
    @web.asynchronous
    def get(self, *args, **kwargs):
        self.required_user_login()
        gen.sleep(10)
        arg_list = {
            'id': 0,
            'passid':self.get_vars['_passid'],
        }

        try:
            self.must_get_args_check(arg_list)
            my_args = self.get_vars
            posts_op = posts.PostOperation(self.Session)
            post_info = posts_op.get_post_by_id(my_args['id'], my_args['passid'])
            if isinstance(post_info, posts.PostInfo):
                return self.finish_out(customErr.CustomErr.success_code, 'success', post_info.get_post())
            else:
                raise customErr.CustomErr(customErr.CustomErr.post_not_find_err, '获取文章失败')
        except Exception as e:
            return self.finish_out(customErr.CustomErr.post_not_find_err, e.__str__())


class GetPostInfoHandler(base.BaseHandler):
    @comm.decorator
    @web.asynchronous
    @gen.coroutine
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

            posts_op = posts.PostOperation(self.Session)

            @gen.coroutine
            def query_list():
                return posts_op.get_posts_list(
                    passid=my_args['passid'],
                    storyid=my_args['storyid'],
                    time_start=int(my_args['starttime']),
                    time_end=int(my_args['endtime']),
                    page=int(my_args['page']),
                    limit=int(my_args['limit']),
                    orderby=my_args['orderby']
                )

            get_res = yield query_list()

            @gen.coroutine
            def get_count():
                return posts_op.get_posts_list_count(
                    passid=my_args['passid'],
                    storyid=my_args['storyid'],
                    time_start=int(my_args['starttime']),
                    time_end=int(my_args['endtime']),
                )

            get_res_count = yield get_count()
            # get_res, get_res_count = yield [query_list(), get_count()]

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

    @comm.decorator
    def get2(self, *args, **kwargs):
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
            tpool = []
            get_res = []
            get_res_count = 0

            def get_list():
                global get_res
                posts_op = posts.PostOperation()
                get_res = posts_op.get_posts_list(
                    passid=my_args['passid'],
                    storyid=my_args['storyid'],
                    time_start=int(my_args['starttime']),
                    time_end=int(my_args['endtime']),
                    page=int(my_args['page']),
                    limit=int(my_args['limit']),
                    orderby=my_args['orderby']
                )

            t = threading.Thread(target=get_list)

            tpool.append(t)

            def count():
                global get_res_count
                posts_op = posts.PostOperation()
                get_res_count = posts_op.get_posts_list_count(
                    passid=my_args['passid'],
                    storyid=my_args['storyid'],
                    time_start=int(my_args['starttime']),
                    time_end=int(my_args['endtime']),
                )

            t2 = threading.Thread(target=count)
            tpool.append(t2)
            for th in tpool:
                th.start()

            for th in tpool:
                th.join()

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
