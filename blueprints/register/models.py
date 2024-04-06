from database import cursor, conn
import bcrypt

def register_user(username, displayname, email, password):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(14))

    cursor.execute("INSERT INTO users (username, displayname, email, password) VALUES (%s, %s, %s, %s)",
                   (username, displayname, email, hashed_password.decode('utf-8')))
    cursor.execute("SELECT id FROM users WHERE username=%s", (username,))
    conn.commit()
    return cursor.fetchone()[0]
