from flask import Flask, jsonify, request, Blueprint
import json

personalInfo_bp = Blueprint('personal_info', __name__)

@personalInfo_bp.route('/completeprofile', methods=["POST"])
def body_measures():
    fields = ["weight","height","age","experience"]
    user_data = json.loads(request.data)

    for field in fields:
        if not field in user_data.keys():
           return jsonify({"message":f"{field} not found"}), 400
        
    #variables
    weight = user_data["weight"]
    height = user_data["height"]
    age = user_data["age"]
    experience = user_data["experience"]

    isValidWeight = is_valid_weight(weight)
    if not isValidWeight:
        return jsonify({"message": "Invalid Weight"}), 400

    isValidHeight = is_valid_height(height)
    if not isValidHeight:
        return jsonify({"message": "Invalid Height"}), 400
    
    isValidAge = is_valid_age(age)
    if not isValidAge:
        return jsonify({"message": "Invalid Age"}), 400

    isValidExperience = is_valid_experience(experience)
    if not isValidExperience:
        return jsonify({"message": "Invalid Experience"}), 400    
    
    return jsonify({"message":"Success"}), 200

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