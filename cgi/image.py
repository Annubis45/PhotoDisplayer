#!/usr/bin/python3
# -*- coding: utf-8 -*

import cgi 
import sys
import requests, json
import os.path

form = cgi.FieldStorage()
idcurrent = form.getvalue("idcurrent")

imageRaw = requests.get("http://localhost:9200/photodisplayer/photo/"+idcurrent)
imageJson = json.loads(imageRaw.text)
fullpath = imageJson["_source"]["fullpath"]
if os.path.exists(fullpath) :
	data = open(fullpath, 'rb').read()

sys.stdout.buffer.write(b"Content-Type: image/jpeg\n\n") 
sys.stdout.buffer.write(data)
