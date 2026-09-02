import random
from datetime import datetime, UTC, timedelta


def generate_otp():
    """Generate a random 6-digit OTP."""
    return str(random.randint(100000, 999999))


def otp_expiry_time():
    """OTP expires in 5 minutes."""
    return datetime.now(UTC) + timedelta(minutes=5)


def otp_is_expired(expiry_time):
    """Return True if OTP has expired."""
    return datetime.now(UTC) > expiry_time