from flask import Flask, jsonify,request,session
import pymongo
import json
from bson import json_util
from flask_cors import CORS
import bcrypt
from itsdangerous import URLSafeTimedSerializer

application = Flask(__name__)
q_client_mongo = pymongo.MongoClient("mongodb+srv://egemen:12345@cluster0.5dvoe.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
mongoDB = q_client_mongo.API

application.secret_key = 'the random string'
CORS(application)



@application.route("/user")
def user():
    inputs = request.args
    email = inputs["email"]  
    if "email" in session:
        res =jsonify(json.loads(json.dumps([element for element in mongoDB.Users.find({"EMAIL":session["email"]},{"_id": 0,"NAME":1,"EMAIL":1,"ACCOUNT_TYPE":1})], default=json_util.default)))
        res.headers.add('Access-Control-Allow-Credentials', 'true')
        return res
    res =jsonify({"status":"Please Login"})
    res.headers.add('Access-Control-Allow-Credentials', 'true')
    return res


@application.route("/register", methods=['post', 'get'])
def register():
    inputs = request.args
    name = inputs["name"]
    email = inputs["email"]
    password = inputs["password"]
    accountType=inputs["accountType"]
    email_found = mongoDB.Users.find_one({"EMAIL": email})
    if email_found:
        res = jsonify(False)
        res.headers.add('Access-Control-Allow-Credentials', 'true')
        return res
    mongoDB.Users.insert_one({
        "NAME" : name,
        "EMAIL" : email,
        "PASSWORD" : bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()),
        "ACCOUNT_TYPE" :accountType
    })
    res = jsonify(True)
    res.headers.add('Access-Control-Allow-Credentials', 'true')
    return res



@application.route("/login", methods=["GET"])
def login():
    if "email" in session:
        res=jsonify({"status":"already logged in","email":session['email']})
        res.headers.add('Access-Control-Allow-Credentials', 'true')
        return res
    inputs=request.args
    email= inputs['email']
    password=inputs['password']
    email_found = mongoDB.Users.find_one({"EMAIL": email})
    if email_found:
        passwordcheck = email_found['PASSWORD']
        if bcrypt.checkpw(password.encode('utf-8'), passwordcheck):
            session["email"]=email_found['EMAIL']
            res=jsonify({"status":"already logged in","email":session['email']})
            res.headers.add('Access-Control-Allow-Credentials', 'true')
            return res
    res=jsonify({"status":"Wrong Mail or Password"})
    res.headers.add('Access-Control-Allow-Credentials', 'true')
    return res



@application.route("/logout", methods=["GET"])
def logout():
    if "email" in session:
        session.pop("email", None)
        res=jsonify("Logged Out")
        res.headers.add('Access-Control-Allow-Credentials', 'true')
        return res
    else:
        res=jsonify("Logged Out")
        res.headers.add('Access-Control-Allow-Credentials', 'true')
        return res


if __name__ == "__main__":
    application.run(port=5000, debug=True)