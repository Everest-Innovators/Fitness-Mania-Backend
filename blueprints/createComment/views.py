from flask import jsonify, request, Blueprint
import json
from psycopg2 import errors as psycopg2_errors
from .models import save_comment_to_db

createComment_bp = Blueprint('create_comment', __name__)
@createComment_bp.route('/comment', methods=["POST"])
def comment():
    fields = ["id", "post_id", "body", "parent_comment_id"]
    comment_data = json.loads(request.data)
    for field in fields:
        if field != "parent_comment_id" and field not in comment_data.keys():
            return jsonify({"message": f"{field} not found"}), 400
        
    id = comment_data["id"]
    post_id = comment_data["post_id"]
    parent_comment_id = comment_data.get("parent_comment_id")
    body = comment_data["body"]

    isTextValid = textChecker(body)
    if not isTextValid["status"]:
        return jsonify({"message": isTextValid["message"]}), 400

    try:
        save_comment_to_db(id, post_id, body, parent_comment_id)
        return jsonify({"message": "Comment Created Successfully"}), 200
    except psycopg2_errors.ForeignKeyViolation as e:
        return jsonify({"message": "Invalid user ID or post ID or parent comment ID"}), 400
    

def textChecker(body):
    if len(body) < 3 or body.isspace():
        return {"status":False, "message":"Your comment is too short. Write at least 3 letters."}
    return {"status":True}