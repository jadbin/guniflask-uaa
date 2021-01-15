# coding=utf-8

from guniflask.orm import BaseModelMixin
from sqlalchemy.dialects.mysql.types import DATETIME
from sqlalchemy.dialects.mysql.types import VARCHAR
from sqlalchemy import text as _text

from uaa import db


class Authority(BaseModelMixin, db.Model):
    __tablename__ = 'authority'

    name = db.Column(VARCHAR(50), primary_key=True)
    description = db.Column(VARCHAR(255))
    created_time = db.Column(DATETIME, server_default=_text("CURRENT_TIMESTAMP"), default=db.func.now())
    user_authorities = db.relationship('UserAuthority', backref=db.backref('authority', lazy='joined'), cascade='all, delete-orphan', lazy='select')
