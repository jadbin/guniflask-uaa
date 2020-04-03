# coding=utf-8

from flask import abort, jsonify
from guniflask.web import blueprint, get_route
from guniflask.security import has_role

from uaa.models import User


@blueprint('/api')
class UserController:

    @get_route('/users/<login>')
    @has_role('admin')
    def get_user_by_login(self, login):
        user = User.query.filter_by(login=login).first()
        if user is None:
            abort(404)
        return jsonify(user.to_dict())
