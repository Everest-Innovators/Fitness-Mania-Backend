from flask import jsonify, request, Blueprint
import json
from database import conn, cursor

getuser_bp = Blueprint('getuser', __name__)

@getuser_bp.route('/getuser/<int:id>', methods=["GET"])
def getuser(id):
    posts = []

    cursor.execute("SELECT username FROM users WHERE id=%s",(id,))

    user =  cursor.fetchone()
    if(user):
        return jsonify(user), 200
    else:
        return jsonify({"message":"Invalid user"}), 400
