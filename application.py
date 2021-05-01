from flask import Flask

application = Flask(__name__)

@application.route("/")
def index():
    return "Your Flask App Works!<br>Yarramı ye beşiktaş"

@application.route("/hello")
def hello():
    return "Hello World!123"

@application.route("/user")
def user():
    res =jsonify({"menu": {
        "username": "egemen",
        "password": "123",
    }})
    res.headers.add('Access-Control-Allow-Credentials', 'true')
    return res


if __name__ == "__main__":
    application.run(port=5000, debug=True)