# views.py
from flask import jsonify, request, Blueprint
import json
from .models import save_user_data_to_db
import bcrypt
from database import cursor, conn

personalInfo_bp = Blueprint('personal_info', __name__)

@personalInfo_bp.route('/completeprofile', methods=["POST"])
def body_measures():
    fields = ["id", "password", "weight", "height", "age", "experience"]
    user_data = json.loads(request.data)

    for field in fields:
        if field not in user_data.keys():
           return jsonify({"message": f"{field} not found"}), 400

    id = user_data["id"]
    password = user_data["password"]
    weight = user_data["weight"]
    height = user_data["height"]
    age = user_data["age"]
    experience = user_data["experience"]

    # Example user authentication
    cursor.execute("SELECT password FROM users WHERE id = %s", (id,))
    hashedPass = cursor.fetchone()[0]
    if not bcrypt.checkpw(password.encode('utf8'),hashedPass.encode('utf8')):
        return jsonify({"message": "Authentication Failed"}), 400

    # Validations
    if not is_valid_weight(weight):
        return jsonify({"message": "Invalid Weight"}), 400

    if not is_valid_height(height):
        return jsonify({"message": "Invalid Height"}), 400
    
    if not is_valid_age(age):
        return jsonify({"message": "Invalid Age"}), 400

    if not is_valid_experience(experience):
        return jsonify({"message": "Invalid Experience"}), 400   

    # Save data to database
    save_user_data_to_db(weight, height, age, experience, id)
    
    return jsonify({"message": "Success"}), 200


def is_valid_weight(weight_str):
    try:
        weight = float(weight_str)
        if 0 < weight < 1000:  # Assuming a reasonable range for weight
            return True
        else:
            return False
    except ValueError:
        return False

def is_valid_age(age_str):
    try:
        age = int(age_str)
        if 0 < age < 100:  # Assuming a reasonable range for age
            return True
        else:
            return False
    except ValueError:
        return False

def is_valid_height(height_str):
    try:
        height = float(height_str)
        if 0 < height < 3:  # Assuming a reasonable range for height (meters)
            return True
        else:
            return False
    except ValueError:
        return False

def is_valid_experience(experience_str):
    try:
        experience = float(experience_str)
        if 0 <= experience <= 100:  # Assuming a reasonable range for experience (years)
            return True
        else:
            return False
    except ValueError:
        return False