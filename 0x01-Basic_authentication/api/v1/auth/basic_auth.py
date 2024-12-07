import base64
import binascii
from api.v1.auth.auth import Auth
from typing import TypeVar

class BasicAuth(Auth):
    """ BasicAuth class.
    """
    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        """ Extracts the Base64 part of the Authorization header.
        """
        if authorization_header is None or not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith('Basic '):
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(self, base64_authorization_header: str) -> str:
        """Decodes a Base64 string to UTF-8.
        
        Args:
            base64_authorization_header (str): The Base64 encoded string.
        
        Returns:
            str: The decoded UTF-8 string or None if input is invalid.
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        
        try:
            # Decode the Base64 string and validate its format
            decoded_bytes = base64.b64decode(base64_authorization_header, validate=True)
            return decoded_bytes.decode('utf-8')
        except (binascii.Error, UnicodeDecodeError):
            return None

    def extract_user_credentials(self, decoded_base64_authorization_header: str) -> (str, str):
        """ Extracts the user credentials from a decoded Base64 string.
        
        Args:
            decoded_base64_authorization_header (str): The decoded Base64 string.
        
        Returns:
            (str, str): A tuple containing the user email and password.
        """
        if decoded_base64_authorization_header is None or not isinstance(decoded_base64_authorization_header, str):
            return (None, None)
        if ':' not in decoded_base64_authorization_header:
            return (None, None)
        
        return tuple(decoded_base64_authorization_header.split(':', 1))

    def user_object_from_credentials(self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """ Returns the User instance based on the email and password.
        
        Args:
            user_email (str): The user email.
            user_pwd (str): The user password.
        
        Returns:
            TypeVar('User'): The User instance or None if user_email or user_pwd is invalid.
        """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        
        from models.user import User
        users = User.search({'email': user_email})
        for user in users:
            if user.is_valid_password(user_pwd):
                return user
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ Returns the User instance based on the Authorization header.
        
        Args:
            request (Request): The request object.
        
        Returns:
            TypeVar('User'): The User instance or None if the Authorization header is invalid.
        """
        authorization_header = self.authorization_header(request)
        if authorization_header is None:
            return None
        
        base64_authorization_header = self.extract_base64_authorization_header(authorization_header)
        if base64_authorization_header is None:
            return None
        
        decoded_base64_authorization_header = self.decode_base64_authorization_header(base64_authorization_header)
        if decoded_base64_authorization_header is None:
            return None
        
        user_email, user_pwd = self.extract_user_credentials(decoded_base64_authorization_header)
        if user_email is None or user_pwd is None:
            return None
        
        return self.user_object_from_credentials(user_email, user_pwd)