#!/usr/bin/python3
# -*- coding: utf-8 -*

import cgi 
import base64

form = cgi.FieldStorage()
print("Content-type: text/html; charset=utf-8\n")



#print(image)
var = 0;
photos = ["DSC_0272.JPG", "DSC_0269.JPG", "DSC_02XX.JPG"]
action = form.getvalue("action")

image = ""

if action=="ban":
	image="ok"

if action=="next":
	var = var+1
	ind = ((var)%len(photos))
	image="image.py?image="+photos[ind]

if action=="previous":
	var = var-1
	ind = ((var)%len(photos))
	image="image.py?image="+photos[ind]


if action=="like":
	image="ok"

if action=="dislike":
	image="ok"

if action=="" or str(action) == "None":
	mon_fichier = open("main.html", "r")
	contenu = mon_fichier.read()
	image=contenu

#print("<!--" +str(action) +"-->")
print(image)

