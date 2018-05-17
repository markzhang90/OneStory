#! /usr/bin/env python
# -*- coding:utf-8 -*-

from app.onestory.service.models.base import OperationBase, Base
import app.onestory.library.customErr as customErr
from sqlalchemy import Column, Integer, String, TEXT


class PostOperation(OperationBase):
    def get_posts_list(self, passid, storyid=None, time_start=None, time_end=None, orderby='desc', limit=10, page=1):
        if passid is None or passid == 0:
            raise customErr.CustomErr(customErr.CustomErr.value_err_code, 'passid required')
        if self.session is None:
            self.load_session()
        query = self.session.query(PostInfo)
        query = query.filter(PostInfo.passid == passid)
        if storyid is not None and storyid != -1:
            query = query.filter(PostInfo.story_id == storyid)
        if time_start is not None and time_start != -1:
            query = query.filter(PostInfo.create_date >= time_start)
        if time_end is not None and time_end != -1:
            query = query.filter(PostInfo.create_date <= time_end)
        if orderby != "desc":
            query = query.order_by(PostInfo.create_date.asc())
        else:
            query = query.order_by(PostInfo.create_date.desc())
        if page < 1:
            page = 1
        if limit < 0:
            limit = 0
        offset = (page - 1) * limit
        query = query.offset(offset)
        query = query.limit(limit)
        res = query.all()
        return res

    def get_posts_list_count(self, passid, storyid=None, time_start=None, time_end=None, orderby='desc'):
        if passid is None or passid == 0:
            raise customErr.CustomErr(customErr.CustomErr.value_err_code, 'passid required')
        if self.session is None:
            self.load_session()
        query = self.session.query(PostInfo)
        query = query.filter(PostInfo.passid == passid)
        if storyid is not None and storyid != -1:
            query = query.filter(PostInfo.story_id == storyid)
        if time_start is not None and time_start != -1:
            query = query.filter(PostInfo.create_date >= time_start)
        if time_end is not None and time_end != -1:
            query = query.filter(PostInfo.create_date <= time_end)
        if orderby != "desc":
            query = query.order_by('create_date asc')
        else:
            query = query.order_by('create_date desc')
        res = query.count()
        return res


class PostInfo(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    story_id = Column(Integer, nullable=False)
    uid = Column(Integer, nullable=False)
    passid = Column(String(255), nullable=False)
    header = Column(String(1024), nullable=False)
    rel = Column(TEXT, nullable=False)
    content = Column(TEXT, nullable=False)
    create_date = Column(Integer, nullable=False)
    update_time = Column(Integer, nullable=False)
    ext = Column(TEXT, nullable=False)

    def __init__(self,
                 pid=None,
                 story_id=None,
                 uid=None,
                 passid=None,
                 header=None,
                 rel=None,
                 content=None,
                 create_date=0,
                 update_time=None,
                 ext=None):
        self.id = pid
        self.story_id = story_id
        self.uid = uid
        self.passid = passid
        self.header = header
        self.rel = rel
        self.content = content
        self.create_date = create_date
        self.update_time = update_time
        self.ext = ext

    def get_post(self):
        return {
            'id': self.id,
            'story_id': self.story_id,
            'passid': self.passid,
            'header': self.header,
            'rel': self.rel,
            'content': self.content,
            'create_date': self.create_date,
            'update_time': self.update_time,
            'ext': self.ext,
        }

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.id)
