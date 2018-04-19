#!/usr/bin/python
# -*- coding: UTF-8 -*-
from app.onestory.controller.base import base
from app.onestory.models.data.mysql import conn
import app.onestory.library.common as comm


class MainHandler(base.BaseHandler):
    @comm.decorator
    def get(self):
        mysql = conn.MySql()
        mysql2 = conn.MySql()
        print(mysql.get_connection())
        print(mysql2.get_connection())
        print(mysql is mysql2)
        self.write('<a href="%s">link to story 1</a>' %
                   self.reverse_url("story", "1"))


class StoryHandler(base.BaseHandler):

    def initialize(self, db):
        self.db = db
        print(self.db)

    def get(self, story_id):
        self.write("this is story %s" % story_id)



