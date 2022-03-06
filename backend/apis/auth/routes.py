from backend.apis.input_validator.validator import (
    is_invalid_company_name,
    is_invalid_email,
    is_invalid_password,
    is_invalid_name,
)
from backend.apis.model.http_error import HttpResponse
from backend.apis.response_handler.decorator import handle_response
from backend.db.helper import add_api_run_limit, add_login_details, get_user, add_user
from backend.db.model.user import User
from backend.log.factory import Logger
from flask import current_app
from werkzeug.security import check_password_hash
from flask import Blueprint, jsonify, request, make_response
import jwt
from datetime import datetime, timedelta
from backend.utils.api_util import get_remote_addr

from backend.utils.constants import (
    API_RUN_LIMIT,
    HTTP_FORBIDDEN,
    HTTP_UNAUTHORIZED,
    ERROR,
    NAME,
    NAME_MAX_LENGTH,
    INPUT_VALIDATION,
    PASSWORD_MAX_LENGTH,
    COMPANY_NAME_MAX_LENGTH,
    HTTP_BAD_REQUEST,
)


auth_bp = Blueprint("auth_bp", __name__)

logger = Logger(__name__)

MISSING_EMAIL_PASSWORD = "MISSING_EMAIL_PASSWORD"
INVALID_USER = "INVALID_USER"
INCORRECT_PASSWORD = "INCORRECT_PASSWORD"
EXPIRES_IN_MINUTES = 60
EXPIRES_IN_SECONDS = EXPIRES_IN_MINUTES * 60


@auth_bp.route("/login", methods=["POST"])
@handle_response
def login():
    # creates dictionary of form data
    auth = request.get_json()
    ip_addr = get_remote_addr(request)
    logger.info(f"Attempting login from ip: [{ip_addr}]")

    if not auth or not auth.get("email") or not auth.get("password"):
        raise HttpResponse(
            message="Either email or password is missing",
            code=MISSING_EMAIL_PASSWORD,
            http_status=HTTP_UNAUTHORIZED,
            type=ERROR,
        )

    user: User = get_user(email=auth.get("email"))

    if not user:
        raise HttpResponse(
            message="User does not exist",
            code=INVALID_USER,
            http_status=HTTP_UNAUTHORIZED,
            type=ERROR,
        )

    if check_password_hash(user.password, auth.get("password")):
        user_id = user.user_id
        # generates the JWT Token
        token = jwt.encode(
            {
                "user_id": user_id,
                "exp": datetime.utcnow() + timedelta(minutes=EXPIRES_IN_MINUTES),
            },
            current_app.config["SECRET_KEY"],
            algorithm="HS256",
        ).decode("utf-8")

        logger.info(
            f"Login successful for user: [{user_id}] and ip_address: [{ip_addr}]"
        )

        # Add login entry
        add_login_details(user_id, ip_addr)

        return make_response(
            jsonify(
                {
                    "message": "success",
                    "token": token,
                    "expires_in": EXPIRES_IN_SECONDS,
                }
            ),
            201,
        )
    raise HttpResponse(
        message="Incorrect password",
        code=INCORRECT_PASSWORD,
        http_status=HTTP_FORBIDDEN,
        type=ERROR,
    )


@auth_bp.route("/signup", methods=["POST"])
@handle_response
def signup():
    # creates a dictionary of the form data
    data = request.get_json()

    # gets name, email and password
    name, email = data.get("name"), data.get("email")
    password = data.get("password")
    company_name = data.get("companyName")
    agree_terms = data.get("agreeTerms")

    message = is_invalid_name(NAME, name, NAME_MAX_LENGTH)
    if message:
        raise HttpResponse(
            message=message,
            code=INPUT_VALIDATION,
            http_status=HTTP_BAD_REQUEST,
            type=ERROR,
        )

    message = is_invalid_email(email)
    if message:
        raise HttpResponse(
            message=message,
            code=INPUT_VALIDATION,
            http_status=HTTP_BAD_REQUEST,
            type=ERROR,
        )

    message = is_invalid_password(password)
    if message:
        raise HttpResponse(
            message=message,
            code=INPUT_VALIDATION,
            http_status=HTTP_BAD_REQUEST,
            type=ERROR,
        )

    # Validate only if entered
    if company_name:
        message = is_invalid_company_name(company_name)
        if message:
            raise HttpResponse(
                message=message,
                code=INPUT_VALIDATION,
                http_status=HTTP_BAD_REQUEST,
                type=ERROR,
            )

    # checking for existing user
    user: User = get_user(email=email)
    if not user:

        user: User = add_user(name, email, password, company_name)
        user_id = user.user_id

        # Init user config upon successful registration
        limit = API_RUN_LIMIT
        add_api_run_limit(user_id, limit)

        response = make_response(
            jsonify({"message": "Successfully registered"}),
            201,
        )
        return response
    else:
        response = make_response(
            jsonify({"message": "User already exists. Please log in"}),
            202,
        )
        return response
