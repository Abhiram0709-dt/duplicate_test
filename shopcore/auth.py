from __future__ import annotations

import hashlib
import secrets

from .models import User


class AuthenticationError(ValueError):
    pass


def hash_password(password: str, salt: str) -> str:
    payload = f"{salt}:{password}".encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


class AuthService:
    def __init__(self) -> None:
        self._users_by_email: dict[str, User] = {}
        self._tokens: dict[str, str] = {}

    def register_user(self, user: User) -> None:
        self._users_by_email[user.email] = user

    def authenticate(self, email: str, password: str) -> str:
        user = self._users_by_email.get(email)
        if user is None:
            raise AuthenticationError("Unknown account")

        if not user.password_hash:
            raise AuthenticationError("Account is not configured for password login")

        expected_hash = hash_password(password=password, salt=user.user_id)
        if expected_hash != user.password_hash:
            raise AuthenticationError("Invalid credentials")

        token = secrets.token_hex(16)
        self._tokens[token] = user.user_id
        return token
