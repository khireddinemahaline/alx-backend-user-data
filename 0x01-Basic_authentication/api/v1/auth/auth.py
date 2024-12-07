#!/usr/bin/env python3

from flask import request
from typing import List, TypeVar, Optional

class Auth:
    """Auth class for handling authentication logic in a Flask application."""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Determine whether a path requires authentication based on a list of excluded paths.

        Args:
            path (str): The request path to check.
            excluded_paths (List[str]): A list of paths that are excluded from authentication.

        Returns:
            bool: True if authentication is required, False if excluded.
        """
        if path is None:
            return True

        if not excluded_paths:
            return True

        # Normalize the path to ensure it's slash-tolerant
        if not path.endswith('/'):
            path += '/'

        for excluded_path in excluded_paths:
            if excluded_path.endswith('/') and path == excluded_path:
                return False

        return True

    def authorization_header(self, request=None) -> Optional[str]:
        """
        Retrieve the 'Authorization' header from a request.

        Args:
            request (Request, optional): The Flask request object.

        Returns:
            str or None: The 'Authorization' header value or None if not found.
        """
        if request is None:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieve the current user from the request.

        Args:
            request (Request, optional): The Flask request object.

        Returns:
            User or None: The current user object, or None if not authenticated.
        """
        return None
