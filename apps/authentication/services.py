from datetime import datetime, UTC

from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password

from config.database.mongodb import db

from .utils import otp_is_expired

from bson import ObjectId



def create_customer(form_data):
    """
    Creates a new customer in MongoDB.
    Raises ValueError if the email already exists.
    """

    email = form_data["email"].lower().strip()

    # Check for duplicate email
    existing_user = db.users.find_one({"email": email})

    if existing_user:
        raise ValueError("An account with this email already exists.")

    user = {
        "first_name": form_data["first_name"],
        "last_name": form_data["last_name"],
        "email": email,
        "phone": form_data["phone"],

        # Never store the plain password.
        "password_hash": make_password(form_data["password"]),

        "role": "customer",
        "status": "pending_verification",

        "mfa_enabled": True,
        "email_verified": False,

        "created_at": datetime.now(UTC),
        "updated_at": datetime.now(UTC),
        "last_login": None,
    }

    result = db.users.insert_one(user)

    return result.inserted_id

def authenticate_customer(email, password):
    """
    Verify a customer's email and password.

    Returns:
        User document if authentication succeeds.

    Raises:
        ValueError if authentication fails.
    """

    email = email.lower().strip()

    user = db.users.find_one({"email": email})

    if not user:
        raise ValueError("Invalid email or password.")

    password_matches = check_password(
        password,
        user["password_hash"]
    )

    if not password_matches:
        raise ValueError("Invalid email or password.")

    return user

def verify_demo_otp(session, submitted_otp):
    """
    Verify the OTP stored in the user's session.

    Raises:
        ValueError if verification fails.

    Returns:
        True if verification succeeds.
    """

    stored_otp = session.get("otp_code")
    expiry_string = session.get("otp_expires")

    if not stored_otp or not expiry_string:
        raise ValueError("Verification session has expired. Please log in again.")

    expiry_time = datetime.fromisoformat(expiry_string)

    if otp_is_expired(expiry_time):
        raise ValueError("Your verification code has expired. Please log in again.")

    if submitted_otp != stored_otp:
        raise ValueError("Invalid verification code.")

    return True

def complete_customer_login(session):
    """
    Complete MFA authentication and update the customer.
    """

    pending_user_id = session.get("pending_user_id")

    if not pending_user_id:
        raise ValueError("Verification session has expired.")

    # Update user status in MongoDB
    db.users.update_one(
        {"_id": ObjectId(pending_user_id)},
        {
            "$set": {
                "status": "active",
                "email_verified": True,
                "last_login": datetime.now(UTC),
                "updated_at": datetime.now(UTC),
            }
        },
    )

    # Rotate session key (security)
    session.cycle_key()

    # Promote pending session → authenticated session
    session["user_id"] = pending_user_id

    # Remove temporary OTP session data
    session.pop("pending_user_id", None)
    session.pop("otp_code", None)
    session.pop("otp_expires", None)

    return pending_user_id