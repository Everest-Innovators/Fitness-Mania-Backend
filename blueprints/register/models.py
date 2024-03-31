from database import cursor, conn
import bcrypt

def register_user(username, displayname, email, password):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(14))

    cursor.execute('DROP TABLE IF EXISTS users;')
    cursor.execute('CREATE TABLE users ('
               'id SERIAL PRIMARY KEY,'
               'username VARCHAR NOT NULL,'
               'displayname VARCHAR NOT NULL,'
               'email VARCHAR NOT NULL,'
               'password VARCHAR NOT NULL,'
               'weight FLOAT DEFAULT 0.0,'
               'height FLOAT DEFAULT 0.0,'
               'age INT DEFAULT 0,'
               'experience INT DEFAULT 0'
               ')'
               )
    cursor.execute("INSERT INTO users (username, displayname, email, password) VALUES (%s, %s, %s, %s)",
                   (username, displayname, email, hashed_password.decode('utf-8')))
    conn.commit()
