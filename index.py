from flask import Flask
from flask_cors import CORS, cross_origin
from blueprints.personalInfo.views import personalInfo_bp
from blueprints.register.views import register_bp
from blueprints.createPost.views import createPost_bp
from blueprints.createComment.views import createComment_bp
from blueprints.reactions.views import react_bp
from blueprints.feed.views import feed_bp
from blueprints.validUser.views import validuser_bp
from blueprints.login.views import login_bp
from blueprints.getuser.views import getuser_bp


# API
app = Flask(__name__)

# cors
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

app.register_blueprint(register_bp)
app.register_blueprint(personalInfo_bp)
app.register_blueprint(createPost_bp)
app.register_blueprint(createComment_bp)
app.register_blueprint(react_bp)
app.register_blueprint(feed_bp)
app.register_blueprint(validuser_bp)
app.register_blueprint(login_bp)
app.register_blueprint(getuser_bp)

@app.route("/")
@cross_origin()
def hello_world():
    return "<p>Hello, World!</p>"

if __name__ == "__main__":
    app.run(debug=True)
