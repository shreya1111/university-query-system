import bcrypt
from typing import Tuple


def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt.

    Args:
        password: The plain-text password to hash.

    Returns:
        A string containing the hashed password.
    """
    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')


def check_password(password: str, hashed: str) -> bool:
    """
    Check a plain-text password against a hashed password.

    Args:
        password: The plain-text password to check.
        hashed: The hashed password string (as returned by hash_password).

    Returns:
        True if the password matches, False otherwise.
    """
    try:
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
    except Exception:
        return False