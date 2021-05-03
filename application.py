from flask import Flask, jsonify,request,session,Flask, render_template, request, url_for, redirect, session, Response, make_response
import pymongo
import json
import flask
from bson import json_util
from flask_cors import CORS


application = flask.Flask(__name__)
q_client_mongo = pymongo.MongoClient("mongodb+srv://egemen:12345@cluster0.5dvoe.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
mongoDB = q_client_mongo.API

CORS(application)

application.config.update( 
    DEBUG=False, 
    SECRET_KEY="65465f4a6s54f6as54g6a54ya687ytq9ew841963684", 
    supports_credentials=True)


@application.route("/deneme")
def deneme():
    res =jsonify({"status":"Application is running"})
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
        "PASSWORD" : password,
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
        if passwordcheck==password:
            session["email"]=email
            res=jsonify({"status":"logged in","email":session['email']})
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


# Couldn't use flask web token because of the server domain
@application.route("/user", methods=["GET"])
def user():
    inputs=request.args
    email= inputs['email']
    if email:
        res =jsonify(json.loads(json.dumps([element for element in mongoDB.Users.find({"EMAIL":email},{"_id": 0,"NAME":1,"EMAIL":1,"ACCOUNT_TYPE":1})], default=json_util.default)))
        res.headers.add('Access-Control-Allow-Credentials', 'true')
        return res
    res =jsonify({"status":"Please Login"})
    res.headers.add('Access-Control-Allow-Credentials', 'true')

    return res

if __name__ == "__main__":
    application.run(port=5000)