from flask import request
from typing import List, TypeVar

class Auth:
    """ Auth class.
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        if path not in excluded_paths or path is None or excluded_paths is None:
            return True
        elif path in excluded_paths:
            return False

    def authorization_header(self, request=None) -> str:
        return None
    def current_user(self, request=None) -> TypeVar('User'):
        return None