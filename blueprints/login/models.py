from database import cursor, conn
import bcrypt

def fetch_user(password, email):
    cursor.execute("SELECT password FROM users WHERE email = %s", (email,))
    if(not cursor.fetchone()):
        return False
    hashedPass = cursor.fetchone()[0]
    if not bcrypt.checkpw(password.encode('utf8'),hashedPass.encode('utf8')):
        return False
    cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
    return cursor.fetchone()[0]
