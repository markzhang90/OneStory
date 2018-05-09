#! /usr/bin/env python
# -*- coding:utf-8 -*-

from app.onestory.service.models.base import OperationBase
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, TEXT

Base = declarative_base()


class PostOperation(OperationBase):

    def insert_alchemy_post(self, post_info):
        if self.session is None:
            self.load_session()
        self.session.add(post_info)
        try:
            self.session.commit(post_info)
        except Exception as e:
            self.session.rollback()
            raise e
        return True


class PostInfo(Base):

    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    story_id = Column(Integer, nullable=False, key=True)
    uid = Column(Integer, nullable=False, key=True)
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
                 header=None,
                 rel=None,
                 content=None,
                 create_date=0,
                 update_time=None,
                 ext=None,):
        self.id = pid
        self.story_id = story_id
        self.uid = uid
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
            'uid': self.uid,
            'header': self.header,
            'rel': self.rel,
            'content': self.content,
            'create_date': self.create_date,
            'update_time': self.update_time,
            'ext': self.ext,
        }
