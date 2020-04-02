# coding=utf-8

from sqlalchemy import text as _text

from uaa import db


class Authority(db.Model):
    __tablename__ = 'authority'

    name = db.Column(db.String(50), primary_key=True)
    description = db.Column(db.String(255))
    created_time = db.Column(db.DateTime, server_default=_text("CURRENT_TIMESTAMP"), default=db.func.now())
    user_authorities = db.relationship('UserAuthority', backref=db.backref('authority', lazy='joined'), cascade='all, delete-orphan', lazy='select')
