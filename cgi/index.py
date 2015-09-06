#!/usr/bin/python3
# -*- coding: utf-8 -*

import cgi 
import base64
import random
import requests, json

def add_note(ajout) :
	headers = {'content-type' : 'application/json'}
	response = requests.get("http://localhost:9200/photodisplayer/current/photo")
	results = json.loads(response.text)
	note = results["_source"]["note"]
	results["_source"]["note"] = note+ajout
	returnJson=results["_source"]
	query2 = json.dumps(returnJson)
	url="http://localhost:9200/photodisplayer/photo/"+results["_source"]["id"];
	response2 = requests.put(url, data=query2)
	print(json.loads(response2.text))

def ban():
	headers = {'content-type' : 'application/json'}
	response = requests.get("http://localhost:9200/photodisplayer/current/photo")
	results = json.loads(response.text)
	note = results["_source"]["note"]
	results["_source"]["note"] = 0
	returnJson=results["_source"]
	query2 = json.dumps(returnJson)
	url="http://localhost:9200/photodisplayer/photo/"+results["_source"]["id"];
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
	returnJson=results["hits"]["hits"][0]["_source"]
	query2 = json.dumps(returnJson)
	url="http://localhost:9200/photodisplayer/current/photo";
	response2 = requests.put(url, data=query2)
	
	

form = cgi.FieldStorage()
print("Content-type: text/html; charset=utf-8\n")

#Init
var = 0;
html = ""




#Get the order
action = form.getvalue("action")
idcurrent = form.getvalue("id")
idprevious = form.getvalue("previous")

#Switch "order"
if action=="ban":
	ban()
	html="ok"

if action=="next":
	getRandom();
	html=random.random()*random.random();

if action=="previous":
	getRandom();
	html=random.random()*random.random();

if action=="like":
	add_note(1)
	html="ok"

if action=="dislike":
	add_note(-1)
	html="ok"

if action=="" or str(action) == "None":
	getRandom();
	mon_fichier = open("main.html", "r")
	contenu = mon_fichier.read()
	html=contenu
	

#Return the content
#print("<!--" +str(action) +"-->")
print(html)




