from database import cursor, conn
import bcrypt

def register_user(username, displayname, email, password):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(14))

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
    cursor.execute("INSERT INTO users (username, displayname, email, password) VALUES (%s, %s, %s, %s)",
                   (username, displayname, email, hashed_password.decode('utf-8')))
    cursor.execute("SELECT id FROM users WHERE username=%s", (username,))
    conn.commit()
    return cursor.fetchone()[0]
