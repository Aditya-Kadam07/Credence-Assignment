from crypt import methods
import os
from flask import Flask, redirect, session, url_for, request, render_template
import pymongo
import os
from pymongo import MongoClient  
from bson import ObjectId 



app = Flask (__name__)
title = "Credence Assignment"
Heading = "Credence Assignment"
app.secret_key = "testing"

client = MongoClient("mongodb://127.0.0.1:27017")
db=client.Credence
movies = db.movies

def redirect_url():    
    return request.args.get('next') or request.referrer or  url_for('library')    

@app.route("/", methods=['post','get'])
@app.route("/library")
def lists ():
    movies_l=movies.find()
    a1= "active"
    return render_template('library.html',a1=a1,t=title,h=Heading,movies=movies_l)

@app.route("/action",methods=["POST"])
def action():
    name = request.values.get("name")
    summary = request.values.get("summary")
    img=request.values.get("img")
  
    movies.insert({ "name":name, "summary":summary, "img":img})
    return redirect("/library")

@app.route("/remove")
def remove():
    key= request.values.get("_id")
    movies.remove({"_id":ObjectId(key)})
    return redirect("/library")

@app.route("/update") 
def update ():
    id=request.values.get("_id")  
    task = movies.find({"_id":ObjectId(id)})
    return render_template("update.html",tasks=task,h=Heading,t=title) 

@app.route("/action2",methods=["POST"])
def action2():
    
    name = request.values.get("name")
    summary=request.values.get("summary")
    img = request.values.get("img")
    id=request.values.get("_id") 
    movies.update({"_id":ObjectId(id)}, {'$set':{ "name":name, "summary":summary, "img":img }})    
    return redirect("/library")

@app.route("/search",methods=["GET"])
def search():
    key=request.values.get("key")
    refer=request.values.get("refer")
    if(key=="_id"):
        movies_l=movies.find({refer:ObjectId(key)})
    else:
        movies_l=movies.find({refer:key})
    return render_template("searchlist.html",movies=movies_l,t=title,h=Heading)


if __name__ == "__main__":
  app.run(port=8084,debug=True)
