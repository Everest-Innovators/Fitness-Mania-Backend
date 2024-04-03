from flask import jsonify, request, Blueprint
import json
from .models import register_user

register_bp = Blueprint('register', __name__)

@register_bp.route("/register", methods=["POST"])
def register():
    if(not request.data):
        return jsonify({"message": "data not found"}), 400

    fields = ["email", "password", "username", "displayname"]
    user_data = json.loads(request.data)

    # Check if every field exists
    for field in fields:
        if field not in user_data.keys():
            return jsonify({"message": f"{field} not found"}), 400

    email = user_data["email"]
    password = user_data["password"]
    username = user_data["username"]
    displayname = user_data["displayname"]

    # Email verification
    is_valid_email = mail_verifier(email)
    if not is_valid_email["status"]:
        return jsonify({"message": is_valid_email["message"]}), 400

    # Username and display name verification
    if len(username) < 3 or len(username) > 30 or ' ' in username:
        return jsonify({"message": "Invalid Username"}), 400
    if len(displayname) < 3 or len(username) > 30 or displayname.isspace():
        return jsonify({"message": "Invalid Display Name"}), 400

    # Password strength check
    is_valid_password = strength_checker(password)
    if not is_valid_password["status"]:
        return jsonify({"message": is_valid_password["message"]}), 400

    # Register user
    id = register_user(username, displayname, email, password)
    return jsonify({"message": "User Registered Successfully", "id": id}), 200


def strength_checker(password_to_check):
        if len(password_to_check) < 8:
            return {"status":False, "message":"Your password should be at least 8 characters long."}
        if len(password_to_check) >= 64:
            return {"status":False, "message":"Your password should not be more than 64 characters long."}
        if sum(1 for c in password_to_check if c.isupper()) <= 0:
             return {"status":False, "message":"Use at least one capital letters."}
        if sum(1 for c in password_to_check if c.islower()) <= 0:
             return {"status":False, "message":"Use at least one small letters."}
        if sum(1 for c in password_to_check if c.isdigit()) <=0:
            return {"status":False, "message":"Use at least one number"}
        return {"status":True}

def mail_verifier(email_to_verify):
     if sum(1 for c in email_to_verify if c=='@') != 1:
         return {"status":False, "message":"Invalid Email"}
     if sum(1 for c in email_to_verify if c=='.') != 1:
         return {"status":False, "message":"Invalid Email"}
     return {"status":True}