# coding=utf-8

from flask import request, abort, jsonify
from guniflask.web import blueprint, post_route
from guniflask.security import has_role

from uaa.config.uaa_config import PasswordEncoder
from uaa.models import User, UserAuthority
from uaa.app import db
from uaa.service.security_contants import SecurityConstants
from uaa.security import security_utils


@blueprint('/api')
class AccountController:

    def __init__(self, password_encoder: PasswordEncoder):
        self.password_encoder = password_encoder

    @post_route('/account')
    @has_role(SecurityConstants.ROLE_ADMIN)
    def create_account(self):
        data = request.json
        if 'login' not in data:
            abort(400, '"login" is required')
        user = User()
        user.login = data['login']
        password = data.get('password')
        if password:
            user.password_hash = self.password_encoder.encode(password.encode('utf-8'))
        user.email = data.get('email')
        user.mobile = data.get('mobile')
        user.nick_name = data.get('nick_name')
        db.session.add(user)
        db.session.commit()

        user_authority = UserAuthority()
        user_authority.user_id = user.id
        user_authority.authority_name = SecurityConstants.ROLE_USER
        db.session.add(user_authority)
        db.session.commit()
        return jsonify(user.to_dict())

    @post_route('/account/change-password')
    def change_password(self):
        data = request.json
        if 'original_password' not in data:
            abort(400, '"original password is required"')
        if 'password' not in data:
            abort(400, '"password is required"')
        login = security_utils.get_current_username()
        user = User.query.filter_by(login=login).first()
        if user is None:
            abort(403, 'No such user')
        if not self.password_encoder.matches(data['original_password'].encode('utf-8'), user.password_hash):
            abort(403, 'Password does not match')
        user.password_hash = self.password_encoder.encode(data['password'].encode('utf-8'))
        db.session.commit()
        return 'success'
