from flask import jsonify, request, Blueprint
import json
from .models import fetch_user

validuser_bp = Blueprint('validuser', __name__)

@validuser_bp.route("/validuser", methods=["POST"])
def register():
    if(not request.data):
        return jsonify({"message": "data not found"}), 400

    fields = ["password", "id"]
    user_data = json.loads(request.data)

    # Check if every field exists
    for field in fields:
        if field not in user_data.keys():
            return jsonify({"message": f"{field} not found"}), 400
    
    id = user_data["id"]
    password = user_data["password"]

    if fetch_user(id,password):
        return jsonify({"message":"Valid"}), 200
    else:
        return jsonify({"message":"Invalid"}), 400