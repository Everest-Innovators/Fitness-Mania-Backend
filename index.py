import json
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/register", methods= ["POST"])
def register():
    data = request.data
    print(data)
    return jsonify({"message":"User Registered Successfully"}), 200