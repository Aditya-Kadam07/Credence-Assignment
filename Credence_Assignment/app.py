from flask import Flask,request,jsonify
from crypt import methods
import os
from cv2 import log
from flask import Flask, redirect, session, url_for, request, render_template
import pymongo
import os
from pymongo import MongoClient  
from bson import ObjectId 
from logging import WARNING, FileHandler
from logging import WARNING, FileHandler







app = Flask (__name__)
title = "Credence Assignment"
Heading = "Credence Assignment"
app.secret_key = "testing"

#Error log file created
file_handler = FileHandler("errorlog.txt")
file_handler.setLevel(WARNING)
app.logger.addHandler(file_handler)


client = MongoClient("mongodb://127.0.0.1:27017")
db=client.Credence
movies = db.movies

#Validation in all the operations is done.
#Output will be displayed in json format.

@app.route("/retrieve", methods=['get'])
def lists ():
    output=[]
    for q in movies.find():
        output.append({"name":q["name"],"summary":q["summary"],"img": q["img"]})
    return jsonify({"result" :output})


@app.route("/search/<name>",methods=["GET"])
def search(name):

    q = movies.find_one({"name": name})

    if q:
        output = {'name' :q["name"],"summary":q["summary"],"img": q["img"]}
    else:
        output = "No such movie Exists"

    return jsonify({"result":output})


@app.route("/action",methods=["POST"])
def action():
    name = request.json["name"]
    summary = request.json["summary"]
    img=request.json["img"]
    q = movies.find_one({"name": name})
    if q: 
        return jsonify({"response":"Movie already exists"})
    else:
        movies_id = movies.insert({ "name":name, "summary":summary, "img":img})
        new_movies = movies.find_one({"_id":movies_id})

    output = {'name' :new_movies["name"],"summary":new_movies["summary"],"img": new_movies["img"]}
    return jsonify({"result":output})


@app.route("/remove",methods=["POST"])
def remove():
    name = request.json["name"]
    if movies.find({"name":name}).count() > 0 :
       movies.remove({"name":name})
       return jsonify({"result" :"Movie "+name +" Deleted Successfully"})
    else:
        
        return jsonify({"response":"Movie not found"})


@app.route("/update",methods=["POST"])
def action2():
    
    name = request.json["name"]
    summary = request.json["summary"]
    img=request.json["img"]
    if movies.find({"name":name}).count() > 0 :
       movies.update({"name":name}, {'$set':{"summary":summary, "img":img }})    
       return jsonify({"result" :"Movie "+name +" Updated Successfully"})
    else:
       return jsonify({"response":"Movie not found"})


#Cannot remove port number, there's an issue on my machine where the port is already in use and it keeps restarting so on my
# machine i have to hard code port number, It should work fine on other machines without mentioning port number
if __name__ == "__main__":
  app.run(port=8084)
