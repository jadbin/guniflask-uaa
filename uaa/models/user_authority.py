# coding=utf-8

from guniflask.orm import BaseModelMixin
from sqlalchemy import text as _text

from uaa import db


class UserAuthority(BaseModelMixin, db.Model):
    __tablename__ = 'user_authority'

    user_id = db.Column(db.BigInteger, db.ForeignKey('user.id'), primary_key=True, nullable=False, index=True)
    authority_name = db.Column(db.String(50), db.ForeignKey('authority.name'), primary_key=True, nullable=False, index=True)
    created_time = db.Column(db.DateTime, server_default=_text("CURRENT_TIMESTAMP"), default=db.func.now())
