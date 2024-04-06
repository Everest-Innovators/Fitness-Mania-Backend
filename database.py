# Database connection
import psycopg2
import os
from dotenv import load_dotenv
load_dotenv()

conn = psycopg2.connect(dbname=os.getenv('DB_NAME'),
                        host=os.getenv('DB_HOST'),
                        user=os.getenv('DB_USER'),
                        password=os.getenv('DB_PASSWORD'),
                        port=os.getenv('DB_PORT'))
cursor = conn.cursor()


cursor.execute("SELECT EXISTS(SELECT relname FROM pg_class WHERE relname = 'users' and relkind='r');")
if(cursor.fetchone()[0] == False):
    cursor.execute('CREATE TABLE users ('
        'id SERIAL PRIMARY KEY,'
        'username VARCHAR NOT NULL UNIQUE,'
        'displayname VARCHAR NOT NULL,'
        'email VARCHAR NOT NULL UNIQUE,'
        'password VARCHAR NOT NULL,'
        'weight FLOAT DEFAULT 0.0,'
        'height FLOAT DEFAULT 0.0,'
        'age INT DEFAULT 0,'
        'experience INT DEFAULT 0'
        ')'
    )
cursor.execute("SELECT EXISTS(SELECT relname FROM pg_class WHERE relname = 'posts' and relkind='r');")
if(cursor.fetchone()[0] == False):
    cursor.execute('CREATE TABLE posts ('
        'post_id SERIAL PRIMARY KEY,'
        'id INTEGER REFERENCES users(id),'
        'title VARCHAR NOT NULL,'
        'body VARCHAR NOT NULL,'
        'media VARCHAR[],'
        'created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,'
         'likers INTEGER[],'
         'dislikers INTEGER[],'
         'comments INTEGER[],'
         'engagement INTEGER'  
         ')'
        )
        
cursor.execute("SELECT EXISTS(SELECT relname FROM pg_class WHERE relname = 'comments' and relkind='r');")
if(cursor.fetchone()[0] == False):
        cursor.execute('CREATE TABLE comments ('
               'comment_id SERIAL PRIMARY KEY,'
               'id INTEGER REFERENCES users(id),'
               'post_id INTEGER REFERENCES posts(post_id),'
               'parent_comment_id INTEGER REFERENCES comments(comment_id),'
               'body VARCHAR NOT NULL,'
               'created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP'
                ')'
               )