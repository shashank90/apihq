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
            {"WWW-Authenticate": 'Basic realm ="Login required !!"'},
        )

    user: User = get_user(email=auth.get("email"))

    if not user:
        # returns 401 if user does not exist
        return make_response(
            "Could not verify",
            401,
            {"WWW-Authenticate": 'Basic realm ="User does not exist !!"'},
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

        return make_response(jsonify({"token": token}), 201)
    # returns 403 if password is wrong
    return make_response(
        "Could not verify",
        403,
        {"WWW-Authenticate": 'Basic realm ="Wrong Password !!"'},
    )


@auth_bp.route("/signup", methods=["POST"])
def signup():
    # creates a dictionary of the form data
    data = request.get_json()

    # gets name, email and password
    name, email = data.get("name"), data.get("email")
    password = data.get("password")

    # checking for existing user
    user: User = get_user(email=email)
    if not user:
        # database ORM object
        add_user(name, email, password)
        return make_response("Successfully registered.", 201)
    else:
        # returns 202 if user already exists
        return make_response("User already exists. Please Log in.", 202)
