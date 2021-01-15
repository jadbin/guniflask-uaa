# coding=utf-8

from guniflask.orm import BaseModelMixin
from sqlalchemy.dialects.mysql.types import DATETIME
from sqlalchemy.dialects.mysql.types import BIGINT
from sqlalchemy.dialects.mysql.types import VARCHAR
from sqlalchemy import text as _text

from uaa import db


class UserAuthority(BaseModelMixin, db.Model):
    __tablename__ = 'user_authority'

    user_id = db.Column(BIGINT(20), db.ForeignKey('user.id'), primary_key=True, nullable=False, index=True)
    authority_name = db.Column(VARCHAR(50), db.ForeignKey('authority.name'), primary_key=True, nullable=False, index=True)
    created_time = db.Column(DATETIME, server_default=_text("CURRENT_TIMESTAMP"), default=db.func.now())
