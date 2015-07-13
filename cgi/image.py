#!/usr/bin/python3
# -*- coding: utf-8 -*

import cgi 
import base64
import sys



form = cgi.FieldStorage()
file1 = form.getvalue("image")

data = open(file1, 'rb').read()

sys.stdout.buffer.write(b"Content-Type: image/jpeg\n\n") 
sys.stdout.buffer.write(data)

