#!/usr/bin/python3
# -*- coding: utf-8 -*

import cgi 
import base64
import random
import requests, json

def getCurrentPhoto(currentPhotoMD5):
	response = requests.get("http://localhost:9200/photodisplayer/photo/"+currentPhotoMD5)
	jsonPhoto = json.loads(response.text)
	return jsonPhoto

def add_note(currentPhotoMD5,ajout) :
	jsonCurrentPhoto=getCurrentPhoto(currentPhotoMD5)
	note = jsonCurrentPhoto["_source"]["note"]
	jsonCurrentPhoto["_source"]["note"] = note+ajout
	returnJson=jsonCurrentPhoto["_source"]
	query2 = json.dumps(returnJson)
	url="http://localhost:9200/photodisplayer/photo/"+jsonCurrentPhoto["_source"]["id"];
	response2 = requests.put(url, data=query2)
	print(json.loads(response2.text))

def ban(currentPhotoMD5):
	jsonCurrentPhoto=getCurrentPhoto(currentPhotoMD5)
	note = jsonCurrentPhoto["_source"]["note"]
	jsonCurrentPhoto["_source"]["note"] = 0
	returnJson=jsonCurrentPhoto["_source"]
	query2 = json.dumps(returnJson)
	url="http://localhost:9200/photodisplayer/photo/"+jsonCurrentPhoto["_source"]["id"];
	response2 = requests.put(url, data=query2)

def getRandom():
	query = json.dumps(
	{
		"query": {
			"function_score": {
				"functions": [
					{
						"random_score": {},
						"weight": 1
					},
					{
						"field_value_factor": {
						"field": "note"
						},
						"weight": 1
					}
					],
				"score_mode": "multiply"
				}
		}
	})
	response = requests.get("http://localhost:9200/photodisplayer/photo/_search?size=1", data=query)
	results = json.loads(response.text)
	photoMD5=results["hits"]["hits"][0]["_source"]["id"]
	return photoMD5
	
	

form = cgi.FieldStorage()
print("Content-type: text/html; charset=utf-8\n")

#Init
var = 0;
html = ""

#Get the action
action = form.getvalue("action")
idcurrent = form.getvalue("id")
idprevious = form.getvalue("previous")

#Switch "action"
if action=="ban":
	ban(idcurrent)
	html="ok"

if action=="next":
	html=getRandom();

if action=="like":
	add_note(idcurrent,1)
	html="ok"

if action=="dislike":
	add_note(idcurrent,-1)
	html="ok"

if action=="" or str(action) == "None":
	getRandom();
	mon_fichier = open("main.html", "r")
	contenu = mon_fichier.read()
	html=contenu
	

#Return the content
#print("<!--" +str(action) +"-->")
print(html)




