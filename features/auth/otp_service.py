import random
from features.auth.password_utils import hash_password, check_password


def generate_otp(length: int = 6) -> str:
    """
    Generate a random OTP of specified length (default 6 digits).

    Args:
        length: The length of the OTP to generate.

    Returns:
        A string of random digits of the specified length.
    """
    return ''.join([str(random.randint(0, 9)) for _ in range(length)])


def hash_otp(otp: str) -> str:
    """
    Hash an OTP using bcrypt.

    Args:
        otp: The OTP string to hash.

    Returns:
        A hashed string suitable for storage.
    """
    return hash_password(otp)


def verify_otp(otp: str, hashed_otp: str) -> bool:
    """
    Verify an OTP against its hash.

    Args:
        otp: The OTP string to verify.
        hashed_otp: The hashed OTP string to compare against.

    Returns:
        True if the OTP matches the hash, False otherwise.
    """
    return check_password(otp, hashed_otp)