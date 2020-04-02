# coding=utf-8

import bcrypt

from guniflask.security import PasswordEncoder


class BcryptPasswordEncoder(PasswordEncoder):
    def encode(self, raw_password: bytes) -> str:
        return bcrypt.hashpw(raw_password, bcrypt.gensalt()).decode('utf-8')

    def matches(self, raw_password: bytes, encoded_password: str) -> bool:
        return bcrypt.checkpw(raw_password, encoded_password.encode('utf-8'))
