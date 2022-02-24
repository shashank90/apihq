from flask import request, jsonify
from flask import current_app

# imports for PyJWT authentication
import jwt
from functools import wraps
from backend.db.helper import get_user

from backend.db.model.user import User

# decorator for verifying the JWT
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # jwt is passed in the request header
        if "x-access-token" in request.headers:
            token = request.headers["x-access-token"]
        # return 401 if token is not passed
        if not token:
            return jsonify({"message": "Token is missing !!"}), 401

        try:
            # decoding the payload to fetch the stored details
            data = jwt.decode(
                token, current_app.config["SECRET_KEY"], algorithms="HS256"
            )
            user_id = data.get("user_id")
            current_user = get_user(user_id=user_id)
        except Exception as e:
            print(e)
            return jsonify({"message": "Token is invalid !!"}), 401
        # returns the current logged in users contex to the routes
        return f(current_user, *args, **kwargs)

    return decorated
