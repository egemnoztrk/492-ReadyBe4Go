from flask import Flask, jsonify,request
import pymongo
import json
from bson import json_util

application = Flask(__name__)
q_client_mongo = pymongo.MongoClient("mongodb+srv://egemen:12345@cluster0.5dvoe.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
mongoDB = q_client_mongo.Users


@application.route("/")
def index():
    return "Your Flask App Works!<br>Yarramı ye beşiktaş"

@application.route("/hello")
def hello():
    return "Hello World!123"

@application.route("/user")
def user():
    res =jsonify(json.loads(json.dumps([element for element in mongoDB.Users.find({},{"_id": 0,"username":1,"password":1})], default=json_util.default)))
    res.headers.add('Access-Control-Allow-Credentials', 'true')
    return res


if __name__ == "__main__":
    application.run(port=5000, debug=True)