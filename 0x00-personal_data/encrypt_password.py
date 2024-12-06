#!/usr/bin/env python3
"""hash_password"""

import bcrypt


def hash_password(password: str) -> bytes:
    """hash_password"""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """is_valid"""
    return bcrypt.checkpw(password.encode(), hashed_password)
