import pyotp
from datetime import datetime, timedelta
import pytz


def generate_otp():
    totp = pyotp.TOTP(pyotp.random_base32(), interval=60)
    otp = totp.now()
    otp_valid_until = datetime.now(tz=pytz.UTC) + timedelta(seconds=60)
    return otp, otp_valid_until


