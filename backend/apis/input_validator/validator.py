from backend.db.helper import get_api_run_count
from marshmallow import validate, ValidationError

from backend.log.factory import Logger
from backend.utils.constants import (
    PASSWORD_MAX_LENGTH,
    COMPANY_NAME_MAX_LENGTH,
    EMAIL_MAX_LENGTH,
)

logger = Logger(__name__)


def is_api_run_limit_exceeded(user_id: str):
    """
    Check if API run limit is exceeded by user
    """
    count, limit = get_api_run_count(user_id)

    if count >= limit:
        return True

    return False


def is_invalid_email(email):
    """
    Test email validity
    """
    try:
        logger.info(f"Validating email...")
        is_invalid_str_length("Email", email, EMAIL_MAX_LENGTH)
        validate.Email(error="Please provide a valid email id")(email)
    except ValidationError as ve:
        return ve.messages
    except Exception as e:
        return str(e)
    return None


def is_invalid_password(value: str):
    """
    Test if string is well-formed
    """
    try:
        logger.info(f"Validating password...")
        is_invalid_str_length("Password", value, PASSWORD_MAX_LENGTH)
        validate.Regexp(
            r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$",
            error="Password must contain minimum eight characters, at least one letter, one number and one special character",
        )(value)
    except ValidationError as ve:
        return ve.messages
    except Exception as e:
        return str(e)
    return None


def is_invalid_company_name(value: str):
    """
    Test company name validity
    """
    try:
        logger.info("Validating company name...")
        is_invalid_str_length("Company name", value, COMPANY_NAME_MAX_LENGTH)
        validate.Regexp(
            r"^[A-Z]([a-zA-Z0-9]|[- @\.#&!])*$",
            error="Company name can contain following special characters only: `.-#&`",
        )(value)
    except ValidationError as ve:
        return ve.messages
    except Exception as e:
        return str(e)
    return None


def is_invalid_name(field_name: str, value: str, length: int):
    """
    Test validity of following:
    1. user name
    2. collection name
    3. file name
    """
    logger.info(f"Validating [{field_name}] with value [{value}]")
    try:
        is_invalid_str_length(field_name, value, length)
        validate.Regexp(
            r"^[a-zA-Z -_]+$",
            error=f"{field_name} can have only hyphen, space or underscore as special characters",
        )(value)
    except ValidationError as ve:
        return ve.messages
    except Exception as e:
        return str(e)
    return None


def is_invalid_str_length(field_name: str, value: str, length: int):
    if len(value) > length:
        raise Exception(f"{field_name} cannot exceed {length} characters")
    return None
