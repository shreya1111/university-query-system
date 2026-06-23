import streamlit as st
from typing import Optional, Tuple, Dict
from .repository import (
    create_user,
    get_user_by_username,
    get_user_by_email,
    get_user_by_id,
    update_user_password,
)
from .password_utils import hash_password, check_password
from .otp_service import generate_otp, hash_otp, verify_otp as verify_otp_hash
from .email_service import EmailService
from .session import set_session, clear_session, init_auth_state


def register_user(username: str, email: str, password: str, role: str, department: str) -> tuple[bool, str]:
    """
    Register a new user.

    Args:
        username: The desired username.
        email: The user's email address.
        password: The plain-text password.
        role: The role (Student, Faculty, Admin).
        department: The department the user belongs to.

    Returns:
        A tuple (success, message). If successful, success is True and message is empty.
        If unsuccessful, success is False and message contains an error description.
    """
    # Initialize auth state (ensures session state variables exist)
    init_auth_state()

    # Basic validation
    if not username or not email or not password or not role or not department:
        return False, "All fields are required"

    if role not in ("Student", "Faculty", "Admin"):
        return False, "Invalid role"

    try:
        user_id = create_user(username, email, password, role, department)
        return True, f"User registered successfully with ID {user_id}"
    except ValueError as e:
        return False, str(e)
    except Exception as e:
        return False, f"Registration failed: {str(e)}"


def login_user(username: str, password: str) -> tuple[bool, str]:
    """
    Authenticate a user and set up the session.

    Args:
        username: The username to authenticate.
        password: The plain-text password to check.

    Returns:
        A tuple (success, message). If successful, success is True and message is empty.
        If unsuccessful, success is False and message contains an error description.
    """
    init_auth_state()

    if not username or not password:
        return False, "Username and password are required"

    # Get user by username
    user = get_user_by_username(username)
    if not user:
        return False, "Invalid username or password"

    # Verify password
    if not check_password(password, user["password_hash"]):
        return False, "Invalid username or password"

    # Set session
    set_session(
        user_id=user["user_id"],
        username=user["username"],
        role=user["role"],
        department=user["department"],
    )
    return True, "Login successful"


def logout_user() -> None:
    """
    Log out the current user by clearing the session.
    """
    clear_session()


def get_current_user() -> Optional[Dict]:
    """
    Get the currently logged-in user's information from session state.

    Returns:
        A dictionary with user information if logged in, None otherwise.
    """
    init_auth_state()
    if not st.session_state.get("logged_in", False):
        return None
    return {
        "user_id": st.session_state.get("user_id"),
        "username": st.session_state.get("username"),
        "role": st.session_state.get("role"),
        "department": st.session_state.get("department"),
    }


# ──────────────────────────────────────────────────────────────────────────
# Password reset (forgot password) flow
#
# Three steps mirror the UI in pages/Forgot_Password.py:
#   1) request_password_reset(email)  → generates an OTP, emails it, stores
#      the hashed OTP in session_state (never the plain OTP).
#   2) verify_otp(email, otp)         → checks the OTP against the stored hash.
#   3) reset_password(email, ...)     → writes the new password to the DB.
# ──────────────────────────────────────────────────────────────────────────


def request_password_reset(email: str) -> tuple[bool, str]:
    """
    Step 1 — look up the user by email, generate a 6-digit OTP, email it,
    and store its hash in session_state keyed by the (lowercased) email.

    Args:
        email: The user's email address.

    Returns:
        A tuple (success, message).
    """
    if not email:
        return False, "Please enter your email address."

    user = get_user_by_email(email.strip())
    if not user:
        # Don't leak whether an account exists.
        return False, "No account found with that email address."

    otp = generate_otp(6)
    # Store only the hash — never the plain OTP.
    st.session_state["pending_otp_hash"] = hash_otp(otp)
    st.session_state["pending_reset_email"] = email.strip()

    try:
        mailer = EmailService()
        sent = mailer.send_email(
            recipient_email=email.strip(),
            subject="Your UniQuery Password Reset Code",
            body=(
                f"Hello {user['username']},\n\n"
                f"Your password reset code is: {otp}\n\n"
                f"This code expires in 10 minutes. If you did not request a "
                f"reset, you can safely ignore this email.\n\n"
                f"— The UniQuery Team"
            ),
        )
    except Exception as e:
        # Email not configured — surface a clear, actionable error.
        return False, f"Unable to send reset email: {e}"

    if not sent:
        return False, "Failed to send the reset email. Please try again."

    return True, "A 6-digit reset code has been sent to your email."


def verify_otp(email: str, otp: str) -> tuple[bool, str]:
    """
    Step 2 — verify the OTP entered by the user against the hash stored
    during step 1.

    Args:
        email: The email that the reset was requested for.
        otp:   The OTP the user entered.

    Returns:
        A tuple (success, message).
    """
    if not otp:
        return False, "Please enter the OTP."

    expected_email = st.session_state.get("pending_reset_email")
    stored_hash = st.session_state.get("pending_otp_hash")

    if not stored_hash or not expected_email:
        return False, "No password reset is in progress. Please start over."

    if email.strip().lower() != expected_email.lower():
        return False, "Email mismatch. Please start the reset process again."

    if not verify_otp_hash(otp.strip(), stored_hash):
        return False, "Incorrect OTP. Please try again."

    # Mark as verified so step 3 can proceed.
    st.session_state["otp_verified"] = True
    return True, "OTP verified. You can now set a new password."


def reset_password(email: str, otp: str, new_password: str) -> tuple[bool, str]:
    """
    Step 3 — validate preconditions, then persist the new password.

    Args:
        email:        The user's email.
        otp:          The OTP (kept for API symmetry / future re-check).
        new_password: The new plain-text password.

    Returns:
        A tuple (success, message).
    """
    if not new_password:
        return False, "Please enter a new password."
    if len(new_password) < 6:
        return False, "Password must be at least 6 characters long."
    if not st.session_state.get("otp_verified"):
        return False, "OTP not verified. Please complete the OTP step first."

    expected_email = st.session_state.get("pending_reset_email")
    if not expected_email or email.strip().lower() != expected_email.lower():
        return False, "Email mismatch. Please start the reset process again."

    new_hash = hash_password(new_password)
    updated = update_user_password(expected_email, new_hash)

    # Clean up reset state regardless of outcome.
    for key in ("pending_otp_hash", "pending_reset_email", "otp_verified"):
        st.session_state.pop(key, None)

    if not updated:
        return False, "Failed to update password. Please try again."

    return True, "Your password has been reset successfully."