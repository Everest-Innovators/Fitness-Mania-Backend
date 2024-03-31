from database import cursor, conn  # we need to setup the database connection in the index.py file

def save_user_data_to_db(weight, height, age, experience, id):
    try:
        # UPDATE DATABASE
        cursor.execute("UPDATE users SET weight = %s, height = %s, age = %s, experience = %s WHERE id = %s",
                       (weight, height, age, experience, id))
        conn.commit()
        print("User data updated successfully.")
    except Exception as e:
        conn.rollback()  # Rollback the transaction if an error occurs
        print(f"Error updating user data: {e}")