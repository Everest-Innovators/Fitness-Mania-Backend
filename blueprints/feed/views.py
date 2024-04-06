from flask import jsonify, request, Blueprint
import json
from database import conn, cursor

feed_bp = Blueprint('feed', __name__)

@feed_bp.route('/latest', methods=["GET"])
def latest_posts():
    posts = []

    cursor.execute("SELECT * FROM posts ORDER BY created_at DESC")

    post = cursor.fetchall()
    for p in post:
        posts.append(p)

    return jsonify(posts)

@feed_bp.route('/top', methods=["GET"])
def top_posts():
    posts = []
    cursor.execute("SELECT * FROM posts ORDER BY engagement DESC")

    post = cursor.fetchall()

    for p in post:
        posts.append(p)

    return jsonify(posts)