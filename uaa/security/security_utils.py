# coding=utf-8

from guniflask.security import UserDetails, SecurityContext


def get_current_username():
    auth = SecurityContext.get_authentication()
    if auth:
        principal = auth.principal
        if isinstance(principal, UserDetails):
            return principal.username
        if isinstance(principal, str):
            return principal
