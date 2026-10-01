import re


def validate_email(email):
    if not email:
        return True
    return bool(re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email))


def sanitize_string(value):
    if value is None:
        return ''
    return str(value).strip()


def normalize_role(role):
    return sanitize_string(role).lower()
