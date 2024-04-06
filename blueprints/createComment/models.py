from database import cursor, conn

def save_comment_to_db(id, post_id, body, parent_comment_id=None):


    
    cursor.execute("INSERT INTO comments (id, post_id, parent_comment_id, body) VALUES (%s, %s, %s, %s) RETURNING comment_id",
                   (id, post_id, parent_comment_id, body))
    comment_id = cursor.fetchone()
    cursor.execute("SELECT comments FROM posts WHERE post_id = %s", (post_id,))
    comments_row = cursor.fetchone()
    if comments_row:
        comments = comments_row[0]
        if comments is None:
            comments = []  # Initialize as an empty list if None
    else:
        comments = []  # Initialize as an empty list if post not found
    comments.append(comment_id)
    cursor.execute("UPDATE posts SET comments = %s WHERE post_id = %s", (comments, post_id))
    conn.commit()
