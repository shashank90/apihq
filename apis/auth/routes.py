import uuid
from db.helper import get_user, add_user
from db.model.user import User
from log.factory import Logger
from flask import current_app
from werkzeug.security import check_password_hash
from flask import Blueprint, jsonify, request, make_response
import jwt
from datetime import datetime, timedelta


auth_bp = Blueprint("auth_bp", __name__)

logger = Logger(__name__)

MISSING_EMAIL_PASSWORD = "MISSING_EMAIL_PASSWORD"
INVALID_USER = "INVALID_USER"
INCORRECT_PASSWORD = "INCORRECT_PASSWORD"

# route for logging user in
@auth_bp.route("/login", methods=["POST"])
def login():
    # creates dictionary of form data
    auth = request.get_json()

    if not auth or not auth.get("email") or not auth.get("password"):
        # returns 401 if any email or / and password is missing
        return make_response(
            "Could not verify",
            401,
            {
                "error": {
                    "code": MISSING_EMAIL_PASSWORD,
                    "message": "Either email or password is missing",
                }
            },
        )

    user: User = get_user(email=auth.get("email"))

    if not user:
        # returns 401 if user does not exist
        return make_response(
            "Could not verify",
            401,
            {"error": {"code": INVALID_USER, "message": "User does not exist"}},
        )

    if check_password_hash(user.password, auth.get("password")):
        # generates the JWT Token
        token = jwt.encode(
            {
                "user_id": user.user_id,
                "exp": datetime.utcnow() + timedelta(minutes=90),
            },
            current_app.config["SECRET_KEY"],
            algorithm="HS256",
        ).decode("utf-8")

        return make_response(jsonify({"message": "success", "token": token}), 201)
    # returns 403 if password is wrong
    return make_response(
        "Could not verify",
        403,
        {"error": {"code": INCORRECT_PASSWORD, "message": "Incorrect password"}},
    )


@auth_bp.route("/signup", methods=["POST"])
def signup():
    # creates a dictionary of the form data
    data = request.get_json()

    # gets name, email and password
    name, email = data.get("name"), data.get("email")
    password = data.get("password")
    company_name = data.get("companyName")

    # checking for existing user
    user: User = get_user(email=email)
    if not user:
        # database ORM object
        add_user(name, email, password, company_name)
        response = make_response(
            jsonify({"message": "Successfully registered"}),
            201,
        )
        # response.headers["Content-Type"] = "application/json"
        return response
    else:
        # returns 202 if user already exists
        response = make_response(
            jsonify({"message": "User already exists. Please log in"}),
            202,
        )
        # response.headers["Content-Type"] = "application/json"
        return response
