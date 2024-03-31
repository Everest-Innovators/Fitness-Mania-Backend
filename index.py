from flask import Flask
from blueprints.personalInfo.views import personalInfo_bp
from blueprints.register.views import register_bp
from blueprints.createPost.views import createPost_bp

# API
app = Flask(__name__)
app.register_blueprint(register_bp)
app.register_blueprint(personalInfo_bp)
app.register_blueprint(createPost_bp)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

if __name__ == "__main__":
    app.run(debug=True)
