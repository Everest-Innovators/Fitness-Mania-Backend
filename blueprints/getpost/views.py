from flask import jsonify, request, Blueprint
import json
from database import conn, cursor

getpost_bp = Blueprint('getpost', __name__)

@getpost_bp.route('/getpost/<int:id>', methods=["GET"])
def getuser(id):

    cursor.execute("SELECT * FROM posts WHERE post_id=%s",(id,))

    post =  cursor.fetchone()
    if(post):
        return jsonify(post), 200
    else:
        return jsonify({"message":"Invalid user"}), 400
