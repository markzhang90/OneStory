#!/usr/bin/python
# -*- coding: UTF-8 -*-
from app.onestory.controller.base import base
from app.onestory.models.data.mysql import conn


class MainHandler(base.BaseHandler):
    def get(self):
        mysql = conn.MySql()
        mysql.get_connection()
        self.write('<a href="%s">link to story 1</a>' %
                   self.reverse_url("story", "1"))


class StoryHandler(base.BaseHandler):

    def initialize(self, db):
        self.db = db
        print(self.db)

    def get(self, story_id):
        self.write("this is story %s" % story_id)



