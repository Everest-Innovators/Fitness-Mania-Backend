from flask import jsonify, request, Blueprint
import json
from database import conn, cursor
from psycopg2 import errors as psycopg2_errors
react_bp = Blueprint('react', __name__)

@react_bp.route('/post/<int:post_id>/like', methods=['POST'])
def like_post(post_id):
    user_id = request.json.get('id')  # Check if user already liked the post
    cursor.execute("SELECT likers FROM posts WHERE post_id = %s", (post_id,))
    likers_row = cursor.fetchone()
    if likers_row:
        likers = likers_row[0]
        if likers is None:
            likers = []  # Initialize as an empty list if None
    else:
        likers = []  # Initialize as an empty list if post not found

    # Check if user already disliked the post
    cursor.execute("SELECT dislikers FROM posts WHERE post_id = %s", (post_id,))
    dislikers_row = cursor.fetchone()
    if dislikers_row:
        dislikers = dislikers_row[0]
        if dislikers is None:
            dislikers = []  # Initialize as an empty list if None
    else:
        dislikers = []  # Initialize as an empty list if post not found

    if user_id in likers:
        # User already liked the post, so unlike it
        likers.remove(user_id)
    else:
        # User didn't like the post, so like it
        likers.append(user_id)
        # Remove user from dislikers if they were in the list
        if user_id in dislikers:
            dislikers.remove(user_id)

    # Update the post record with the new likers list
    cursor.execute("UPDATE posts SET likers = %s, dislikers = %s WHERE post_id = %s", (likers, dislikers, post_id))
    conn.commit()

    return jsonify({"message": "Post liked successfully"}), 200

@react_bp.route('/post/<int:post_id>/dislike', methods=['POST'])
def dislike_post(post_id):
    user_id = request.json.get('id')

    # Check if user already disliked the post
    cursor.execute("SELECT dislikers FROM posts WHERE post_id = %s", (post_id,))
    dislikers_row = cursor.fetchone()
    if dislikers_row:
        dislikers = dislikers_row[0]
        if dislikers is None:
            dislikers = []  # Initialize as an empty list if None
    else:
        dislikers = []  # Initialize as an empty list if post not found

    # Check if user already liked the post
    cursor.execute("SELECT likers FROM posts WHERE post_id = %s", (post_id,))
    likers_row = cursor.fetchone()
    if likers_row:
        likers = likers_row[0]
        if likers is None:
            likers = []  # Initialize as an empty list if None
    else:
        likers = []  # Initialize as an empty list if post not found

    if user_id in dislikers:
        # User already disliked the post, so undislike it
        dislikers.remove(user_id)
    else:
        # User didn't dislike the post, so dislike it
        dislikers.append(user_id)
        # Remove user from likers if they were in the list
        if user_id in likers:
            likers.remove(user_id)

    # Update the post record with the new dislikers and likers lists
    cursor.execute("UPDATE posts SET dislikers = %s, likers = %s WHERE post_id = %s", (dislikers, likers, post_id))
    conn.commit()

    return jsonify({"message": "Post disliked successfully"}), 200