import os
from dotenv import load_dotenv
import psycopg2
import json
from flask import Flask, jsonify, request
import bcrypt

app = Flask(__name__)

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
    if(len(username)<3 or ' ' in username):
        return jsonify({"message": "Invalid Username"}), 400
    if(len(displayname)<3 or displayname.isspace()):
        return jsonify({"message": "Invalid Display Name"}), 400

    # password strength
    isValidPassword = strength_checker(password)
    if not isValidPassword["status"]:
        return jsonify({"message": isValidPassword["message"]}), 400

    # encrypt the password
    hashed = bcrypt.hashpw(bytes(password, 'utf-8'), bcrypt.gensalt())

    return jsonify({"message":"User Registered Successfully"}), 200
    



def strength_checker(password_to_check):
        if len(password_to_check) < 8:
            return {"status":False, "message":"Your password should be at least 8 characters long."}
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