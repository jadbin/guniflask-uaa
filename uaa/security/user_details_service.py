# coding=utf-8

from guniflask.context import service
from guniflask.security import UserDetailsService as GUserDetailsService, UserDetails, User as GUser, \
    UsernameNotFoundError

from uaa.models import User


@service
class UserService(GUserDetailsService):

    def load_user_by_username(self, username: str) -> UserDetails:
        user = User.query.filter_by(login=username).first()
        if user is None:
            raise UsernameNotFoundError
        authorities = set()
        for ua in user.user_authorities:
            authorities.add(ua.authority_name)
        return GUser(username=username, password=user.password_hash, authorities=authorities)
