from flask import request
from typing import List, TypeVar



class Auth:
    """ Auth class.
    """
    def require_auth(self, path: str, excluded_paths: list) -> bool:
        # Return True if path is None
        if path is None:
            return True

        # Return True if excluded_paths is None or empty
        if not excluded_paths:
            return True

        # Normalize the path to ensure it's slash-tolerant
        if not path.endswith('/'):
            path += '/'

        # Check if path matches any excluded path
        for excluded_path in excluded_paths:
            if excluded_path.endswith('/') and path == excluded_path:
                return False

        return True


    def authorization_header(self, request=None) -> str:
        """ authorization_header
        """
        if request is None:
            return None
        elif request.headers.get('Authorization') is None:
            return None
        else:
            return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """ current_user
        """
        return None