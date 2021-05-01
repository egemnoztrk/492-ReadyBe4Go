from flask import Flask

application = Flask(__name__)

@application.route("/")
def index():
    return "Your Flask App Works!<br>Yarramı ye beşiktaş"

@application.route("/hello")
def hello():
    return "Hello World!"


if __name__ == "__main__":
    application.run(port=5000, debug=True)