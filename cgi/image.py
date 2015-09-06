#!/usr/bin/python3
# -*- coding: utf-8 -*

import cgi 
import base64
import sys
import requests, json


query = json.dumps(
{
	"query": { "match_all": {} }
})
response = requests.get("http://localhost:9200/photodisplayer/current/photo")
results = json.loads(response.text)


fullpath = results["_source"]["fullpath"]

#form = cgi.FieldStorage()
#file1 = form.getvalue("image")
data = open(fullpath, 'rb').read()
sys.stdout.buffer.write(b"Content-Type: image/jpeg\n\n") 
sys.stdout.buffer.write(data)
