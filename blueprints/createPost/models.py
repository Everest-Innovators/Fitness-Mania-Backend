from database import cursor, conn

def save_post_to_db(id, title, body, media):

    cursor.execute("SELECT EXISTS(SELECT relname FROM pg_class WHERE relname = 'posts' and relkind='r');")
    if(cursor.fetchone()[0] == False):
        cursor.execute('CREATE TABLE posts ('
               'post_id SERIAL PRIMARY KEY,'
               'id INTEGER REFERENCES users(id),'
               'title VARCHAR NOT NULL,'
               'body VARCHAR NOT NULL,'
               'media VARCHAR[],'
               'created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,'
                'likers INTEGER[],'
                'dislikers INTEGER[]' 
                ')'
               )
        
    media_array_string = "{" + ",".join(media) + "}"
    cursor.execute("INSERT INTO posts (id, title, body, media) VALUES (%s, %s, %s, %s)",
                   (id, title, body, media_array_string))
    conn.commit()
