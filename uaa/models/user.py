# coding=utf-8

from guniflask.orm import BaseModelMixin
from sqlalchemy.dialects.mysql.types import DATETIME
from sqlalchemy.dialects.mysql.types import BIGINT
from sqlalchemy.dialects.mysql.types import VARCHAR
from sqlalchemy import text as _text

from uaa import db


class User(BaseModelMixin, db.Model):
    __tablename__ = 'user'

    id = db.Column(BIGINT(20), primary_key=True, autoincrement=True)
    login = db.Column(VARCHAR(50), nullable=False, unique=True, index=True)
    password_hash = db.Column(VARCHAR(60))
    email = db.Column(VARCHAR(100), unique=True, index=True)
    mobile = db.Column(VARCHAR(20), unique=True, index=True)
    nick_name = db.Column(VARCHAR(50))
    created_time = db.Column(DATETIME, server_default=_text("CURRENT_TIMESTAMP"), default=db.func.now())
    updated_time = db.Column(DATETIME, server_default=_text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), default=db.func.now(), onupdate=db.func.now())
    user_authorities = db.relationship('UserAuthority', backref=db.backref('user', lazy='joined'), cascade='all, delete-orphan', lazy='select')
