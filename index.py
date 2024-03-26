# database connection
import os
from dotenv import load_dotenv
import psycopg2
load_dotenv()
conn = psycopg2.connect(dbname=os.getenv('DB_NAME'),
                        host=os.getenv('DB_HOST'),
                        user=os.getenv('DB_USER'),
                        password=os.getenv('DB_PASSWORD'),
                        port=os.getenv('DB_PORT'))
cursor = conn.cursor()
# check if table is created
cursor.execute("SELECT EXISTS(SELECT relname FROM pg_class WHERE relname = 'users' and relkind='r');")
if(cursor.fetchone()[0] == False):
    cursor.execute("CREATE TABLE users (id serial primary key, username varchar(30), displayname varchar(30), email varchar, password varchar, weight float, height float, age int, experience int)")
conn.commit()



# API
import json
from flask import Flask, jsonify, request, Blueprint
import bcrypt
from blueprints.personal_info import body_measures
from blueprints.personal_info import personalInfo_bp

app = Flask(__name__)
app.register_blueprint(personalInfo_bp)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


fields = ["email","password","username","displayname"]
@app.route("/register", methods= ["POST"])
def register():
    user_data = json.loads(request.data)

    # check if every field exists
    for field in fields:
        if not field in user_data.keys():
           return jsonify({"message":f"{field} not found"}), 400

    # variables
    email = user_data["email"]
    password = user_data["password"]
    username = user_data["username"]
    displayname = user_data["displayname"]

    # email verify
    isValidEmail = mail_verifier(email)
    if not isValidEmail["status"]:
        return jsonify({"message": isValidEmail["message"]}), 400

    # username and display name verify
    if(len(username)<3 or len(username)>30 or ' ' in username):
        return jsonify({"message": "Invalid Username"}), 400
    if(len(displayname)<3 or len(username)>30 or displayname.isspace()):
        return jsonify({"message": "Invalid Display Name"}), 400

    # password strength
    isValidPassword = strength_checker(password)
    if not isValidPassword["status"]:
        return jsonify({"message": isValidPassword["message"]}), 400

    # encrypt the password
    hashed = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt(14))
    

    # upload it to database
    cursor.execute("INSERT INTO users (username,displayname,email,password) VALUES(%s,%s,%s,%s)",(username,displayname,email,hashed.decode('utf8')))
    conn.commit()

    return jsonify({"message":"User Registered Successfully"}), 200
    

def strength_checker(password_to_check):
        if len(password_to_check) < 8:
            return {"status":False, "message":"Your password should be at least 8 characters long."}
        if len(password_to_check) >= 64:
            return {"status":False, "message":"Your password should not be more than 64 characters long."}
        if sum(1 for c in password_to_check if c.isupper()) <= 0:
             return {"status":False, "message":"Use at least one capital letters."}
        if sum(1 for c in password_to_check if c.islower()) <= 0:
             return {"status":False, "message":"Use at least one small letters."}
        if sum(1 for c in password_to_check if c.isdigit()) <=0:
            return {"status":False, "message":"Use at least one number"}
        return {"status":True}

def mail_verifier(email_to_verify):
     if sum(1 for c in email_to_verify if c=='@') != 1:
         return {"status":False, "message":"Invalid Email"}
     if sum(1 for c in email_to_verify if c=='.') != 1:
         return {"status":False, "message":"Invalid Email"}
     return {"status":True}