import json
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/register", methods= ["POST"])
def register():
    user_data = json.loads(request.data)
    print(user_data["password"])
    print(strength_checker(user_data["password"]))
    return jsonify({"message":"User Registered Successfully"}), 200



def strength_checker(password_to_check):
        if len(password_to_check) < 8:
            return {"status":False, "message":"Your password should be at least 8 characters long."}
        if sum(1 for c in password_to_check if c.isupper()) <= 0:
             return {"status":False, "message":"Use at least one capital letters."}
        if sum(1 for c in password_to_check if isinstance(c, int)) <=0:
            return {"status":False, "message":"Use at least one number"}
        return {"status":True}

def mail_verifier(email_to_verify):
     if sum(1 for c in email_to_verify if c=='@') != 1:
          return jsonify({"message":"Invalid email"}),200
     return True