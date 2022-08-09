# flask imports
from flask import Flask, request, jsonify, make_response, json
from flask_sqlalchemy import SQLAlchemy
import uuid  # for public id
from werkzeug.security import generate_password_hash, check_password_hash

# imports for PyJWT authentication
import jwt
from datetime import datetime, timedelta
from functools import wraps
from src.sql.sqlite import User
from src.server.flask_server import app, db


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
            return jsonify(
                {
                    "message": """Error 401; Token is missing.
                                        Please authenticate and pass token in the header with
                                        key x-access-token:<<your_token>>"""
                }
            )
        try:
            # decoding the payload to fetch the stored details

            data = jwt.decode(token, app.config["SECRET_KEY"])
            current_user = User.query.filter_by(public_id=data["public_id"]).first()
        except:
            return jsonify({"message": "Token is invalid !!"}), 401
        # returns the current logged in users contex to the routes
        return f(current_user, *args, **kwargs)

    return decorated
