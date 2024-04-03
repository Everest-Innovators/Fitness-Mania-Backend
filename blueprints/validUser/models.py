from database import cursor, conn
import bcrypt

def fetch_user(id, password):
    cursor.execute("SELECT password FROM users WHERE id = %s", (id,))
    hashedPass = cursor.fetchone()[0]
    if not bcrypt.checkpw(password.encode('utf8'),hashedPass.encode('utf8')):
        return False
    return True
