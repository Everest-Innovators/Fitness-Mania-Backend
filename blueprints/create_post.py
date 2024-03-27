from flask import Flask, jsonify, request, Blueprint
import json
# from index import cursor, conn
import bcrypt

createPost_bp = Blueprint('create_post', __name__)

@createPost_bp.route('/completeprofile', methods=["POST"])
def body_measures():
    fields = ["id","password","title","body"]
    user_data = json.loads(request.data)

    for field in fields:
        if not field in user_data.keys():
           return jsonify({"message":f"{field} not found"}), 400
        
    # variables
    id = user_data["id"]
    password = user_data["password"]
    title = user_data["title"]
    body = user_data["body"]

    # fetch user and check password
    # cursor.execute("SELECT password FROM users WHERE id=%s",id)
    # hashedPass = cursor.fetchone()[0]
    # if not bcrypt.checkpw(password.encode('utf8'),hashedPass.encode('utf8')):
    #     return jsonify({"message": "Authentication Failed"}), 400
    
    return jsonify({"message":"Success"})
    
        
