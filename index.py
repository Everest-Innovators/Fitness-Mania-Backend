import json
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/register", methods= ["POST"])
def register():
    user_data = request.get_json()
    return jsonify({"message":"User Registered Successfully"}), 200

def strength_checker(user_data):
        password_to_check = user_data.password
        if len(password_to_check) < 8:
            return jsonify({"message":"Your password should be at least 8 characters long."}),200
        if sum(1 for c in password_to_check if c.isupper()) <= 0:
             return jsonify({"message":"Use at least one capital letters."}), 200
        if sum(1 for c in password_to_check if isinstance(c, int)) <=0:
            return jsonify({"message":"Use at least one number"})
        return True, 200

def mail_verifier(user_data):
     email_to_verify = user_data.email
     if sum(1 for c in email_to_verify if c=='@') != 1:
          return jsonify({"message":"Invalid email"}),200
     return True