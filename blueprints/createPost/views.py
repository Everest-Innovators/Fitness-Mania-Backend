from flask import jsonify, request, Blueprint
import json
from .models import save_post_to_db

createPost_bp = Blueprint('create_post', __name__)
@createPost_bp.route('/post', methods=["POST"])
def post():
    fields = ["id", "title", "body", "media"]
    post_data = json.loads(request.data)
    for field in fields:
        if field != "media" and field not in post_data.keys():
            return jsonify({"message": f"{field} not found"}), 400
        
    id = post_data["id"]
    title = post_data["title"]
    body = post_data["body"]
    media_data = post_data.get("media", [])

    isTextValid = textChecker(title, body)
    if not isTextValid["status"]:
        return jsonify({"message": isTextValid["message"]}), 400

    save_post_to_db(id, title, body, media_data)
    return jsonify({"message": "Post Created Successfully"}), 200

def textChecker(title, body):
    if len(title) < 10 or title.isspace():
        return {"status":False, "message":"Your title is too short. Write at least 10 letters."}
    if len(body) < 3 or body.isspace():
        return {"status":False, "message":"Your body is too short. Write at least 3 letters."}
    return {"status":True}