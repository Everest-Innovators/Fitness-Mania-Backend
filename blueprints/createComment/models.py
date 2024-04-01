from database import cursor, conn

def save_comment_to_db(id, post_id, body, parent_comment_id=None):

    cursor.execute("SELECT EXISTS(SELECT relname FROM pg_class WHERE relname = 'comments' and relkind='r');")
    if(cursor.fetchone()[0] == False):
        cursor.execute('CREATE TABLE comments ('
               'comment_id SERIAL PRIMARY KEY,'
               'id INTEGER REFERENCES users(id),'
               'post_id INTEGER REFERENCES posts(post_id),'
               'parent_comment_id INTEGER REFERENCES comments(comment_id),'
               'body VARCHAR NOT NULL,'
               'created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP'
                ')'
               )
    
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
