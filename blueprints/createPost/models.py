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
                'dislikers INTEGER[],'
                'comments INTEGER[],'
                'engagement INTEGER'  
                ')'
               )
        
        #to calculate engagement
        cursor.execute('''
            CREATE OR REPLACE FUNCTION calculate_engagement() RETURNS TRIGGER AS $$
            BEGIN
                NEW.engagement := (SELECT COALESCE(array_length(NEW.likers, 1), 0) + 
                                   COALESCE(array_length(NEW.dislikers, 1), 0) + 
                                   COALESCE(array_length(NEW.comments, 1), 0));
                RETURN NEW;
            END;
            $$ LANGUAGE plpgsql;
        ''')
        
        #trigger to update engagement
        cursor.execute('''
            CREATE TRIGGER update_engagement
            BEFORE INSERT OR UPDATE OF likers, dislikers, comments ON posts
            FOR EACH ROW EXECUTE FUNCTION calculate_engagement();
        ''')
        
    media_array_string = "{" + ",".join(media) + "}"
    cursor.execute("INSERT INTO posts (id, title, body, media) VALUES (%s, %s, %s, %s)",
                   (id, title, body, media_array_string))
    conn.commit()
