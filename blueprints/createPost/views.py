from flask import jsonify, request, Blueprint
import json
from psycopg2 import errors as psycopg2_errors
from .models import save_post_to_db
from database import cursor, conn
import bcrypt

createPost_bp = Blueprint('create_post', __name__)
@createPost_bp.route('/post', methods=["POST"])
def post():
    fields = ["id", "title", "body", "media", "password"]
    post_data = json.loads(request.data)
    for field in fields:
        if field != "media" and field not in post_data.keys():
            return jsonify({"message": f"{field} not found"}), 400
        
    id = post_data["id"]
    password = post_data["password"]
    title = post_data["title"]
    body = post_data["body"]
    media_data = post_data.get("media", [])

    # Example user authentication
    cursor.execute("SELECT password FROM users WHERE id = %s", (id,))
    hashedPass = cursor.fetchone()[0]
    if not bcrypt.checkpw(password.encode('utf8'),hashedPass.encode('utf8')):
        return jsonify({"message": "Authentication Failed"}), 401

    isTextValid = textChecker(title, body)
    if not isTextValid["status"]:
        return jsonify({"message": isTextValid["message"]}), 400

    
    try:
        save_post_to_db(id, title, body, media_data)
        return jsonify({"message": "Post Created Successfully"}), 200
    except psycopg2_errors.ForeignKeyViolation as e:
        return jsonify({"message": "Invalid user ID or post ID"}), 400

def textChecker(title, body):
    if len(title) < 10 or title.isspace():
        return {"status":False, "message":"Your title is too short. Write at least 10 letters."}
    if len(title) > 50:
        return {"status":False, "message":"Your title is too long."}
    if len(body) > 10000:
        return {"status":False, "message":"Your body is too long."}
    if len(body) < 3 or body.isspace():
        return {"status":False, "message":"Your body is too short. Write at least 3 letters."}
    return {"status":True}