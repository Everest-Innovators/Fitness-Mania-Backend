from flask import jsonify, request, Blueprint
import json
from .models import fetch_user

login_bp = Blueprint('login', __name__)

@login_bp.route("/login", methods=["POST"])
def register():
    if(not request.data):
        return jsonify({"message": "data not found"}), 400

    fields = ["password", "email"]
    user_data = json.loads(request.data)

    # Check if every field exists
    for field in fields:
        if field not in user_data.keys():
            return jsonify({"message": f"{field} not found"}), 400
    
    email = user_data["email"]
    password = user_data["password"]
    id = fetch_user(password,email)
    if id:
        return jsonify({"message":"Logged In", "id": id}), 200
    else:
        return jsonify({"message":"Invalid"}), 400