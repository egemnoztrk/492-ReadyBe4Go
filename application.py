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


@application.route("/userSettings", methods=['post', 'get'])
def userSettings():
    inputs = request.args
    email = inputs["email"]
    res=jsonify(json.loads(json.dumps([element for element in mongoDB.Users.find({"EMAIL":email},{"_id": 0,"NAME":1,"SURNAME":1,"PHONE":1,"HES":1,"CITY":1,"ADDRESS":1,"CARD":1,"EMAIL":1,"PASSWORD":1,"ACCOUNT_TYPE":1,"CARD-OWNER":1,"CVC":1})], default=json_util.default)))
    res.headers.add('Access-Control-Allow-Credentials', 'true')
    return res

@application.route("/restaurantSettings", methods=['post', 'get'])
def restaurantSettings():
    inputs = request.args
    email = inputs["email"]
    res=jsonify(json.loads(json.dumps([element for element in mongoDB.Users.find({"EMAIL":email},{"_id": 0,"NAME":1,"DESCRIPTION":1,"AMOUNT":1,"PHONE":1,"CITY":1,"ADDRESS":1,"EMAIL":1,"PASSWORD":1,"ACCOUNT_TYPE":1,"RESERVATION_HOURS":1})], default=json_util.default)))
    res.headers.add('Access-Control-Allow-Credentials', 'true')
    return res

@application.route("/restaurantSettingsSave", methods=['post', 'get'])
def restaurantSettingsSave():
    inputs = request.args
    NAME = inputs["NAME"]
    PHONE = inputs["PHONE"]
    CITY = inputs["CITY"]
    ADDRESS = inputs["ADDRESS"]
    EMAIL = inputs["EMAIL"]
    timeTable = {"10:00-11:00":inputs["time1"],"11:00-12:00":inputs["time2"],"12:00-13:00":inputs["time3"],"13:00-14:00":inputs["time4"],"14:00-15:00":inputs["time5"],"15:00-16:00":inputs["time6"],"16:00-17:00":inputs["time7"],"17:00-18:00":inputs["time8"],"18:00-19:00":inputs["time9"],"19:00-20:00":inputs["time10"],"20:00-21:00":inputs["time11"],"21:00-22:00":inputs["time12"],"22:00-23:00":inputs["time13"],"23:00-24:00":inputs["time14"]}
    mongoDB.Users.update_one({"EMAIL":EMAIL},{"$set":{"NAME":NAME,"PHONE":PHONE,"CITY":CITY,"ADDRESS":ADDRESS,"EMAIL":EMAIL,"DESCRIPTION":inputs["DESCRIPTION"],"AMOUNT":inputs["AMOUNT"],"RESERVATION_HOURS":timeTable}})
    res=jsonify({"status":"done"})
    res.headers.add('Access-Control-Allow-Credentials', 'true')
    return res

@application.route("/getRestaurants", methods=['post', 'get'])
def getRestaurants():
    res=jsonify(json.loads(json.dumps([element for element in mongoDB.Users.find({"ACCOUNT_TYPE":"Restaurant"},{"_id":0,"NAME":1,"PHONE":1,"CITY":1,"RESERVATION_HOURS":1,"ADDRESS":1,"AMOUNT":1,"DESCRIPTION":1}).sort("NAME" , 1)], default=json_util.default)))
    res.headers.add('Access-Control-Allow-Credentials', 'true')
    return res


@application.route("/userSettingsSave", methods=['post', 'get'])
def userSettingsSave():
    inputs = request.args
    NAME = inputs["NAME"]
    SURNAME = inputs["SURNAME"]
    PHONE = inputs["PHONE"]
    HES = inputs["HES"]
    CITY = inputs["CITY"]
    ADDRESS = inputs["ADDRESS"]
    CARD = inputs["CARD"]
    EMAIL = inputs["EMAIL"]
    CARDOWNER = inputs["CARD-OWNER"]
    CVC = inputs["CVC"]
    mongoDB.Users.update_one({"EMAIL":EMAIL},{"$set":{"NAME":NAME,"SURNAME":SURNAME,"PHONE":PHONE,"HES":HES,"CITY":CITY,"ADDRESS":ADDRESS,"CARD":CARD,"EMAIL":EMAIL,"CARD-OWNER":CARDOWNER,"CVC":CVC}})
    res=jsonify({"status":"done"})
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
    if accountType=="User":
        mongoDB.Users.insert_one({
            "NAME" : name,
            "SURNAME" : "",
            "PHONE" : "",
            "HES" : "",
            "CITY" : "",
            "ADDRESS" : "",
            "CARD" : "",
            "CARD-OWNER" : "",
            "CVC" : "",
            "EMAIL" : email,
            "PASSWORD" : password,
            "ACCOUNT_TYPE" :accountType
        })
    if accountType=="Restaurant":
            mongoDB.Users.insert_one({
            "NAME" : name,
            "DESCRIPTON":"",
            "PHONE" : "",
            "CITY" : "",
            "RESERVATION_HOURS" : "",
            "ADDRESS" : "",
            "EMAIL" : email,
            "PASSWORD" : password,
            "ACCOUNT_TYPE" :accountType
        })
    res = jsonify(True)
    res.headers.add('Access-Control-Allow-Credentials', 'true')

    return res



@application.route("/login", methods=["GET"])
def login():
    inputs=request.args
    email= inputs['email']
    password=inputs['password']
    email_found = mongoDB.Users.find_one({"EMAIL": email})
    if email_found:
        passwordcheck = email_found['PASSWORD']
        if passwordcheck==password:
            res=jsonify(json.loads(json.dumps([element for element in mongoDB.Users.find({"EMAIL":email},{"_id": 0,"ACCOUNT_TYPE":1})], default=json_util.default)))
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