import re
from app.core.exceptions import PasswordNotValid, PasswordTooShort

password_regex = re.compile(
    r"^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.*[#?!@$%^&*-]).+$"
)

def validate_password_strength(password: str):
    if len(password) < 8:
        raise PasswordTooShort()

    if password_regex.fullmatch(password) is None:
        raise PasswordNotValid()
    
    return password