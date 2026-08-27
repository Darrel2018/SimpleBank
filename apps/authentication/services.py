from datetime import datetime, UTC

from django.contrib.auth.hashers import make_password

from config.database.mongodb import db


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