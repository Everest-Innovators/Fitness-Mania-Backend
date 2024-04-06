from flask import jsonify, request, Blueprint
import json
from database import conn, cursor

getcomments_bp = Blueprint('getcomments', __name__)

@getcomments_bp.route('/getcomments/<int:id>', methods=["GET"])
def getcomments(id):

    cursor.execute("SELECT * FROM comments WHERE post_id=%s",(id,))

    comments =  cursor.fetchall()
    if(comments):
        return jsonify(comments), 200
    else:
        return jsonify({"message":"Invalid Post"}), 400
