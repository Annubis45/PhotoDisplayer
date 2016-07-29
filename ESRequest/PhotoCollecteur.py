#!/usr/bin/python3
# -*- coding: utf-8 -*


import sys
import os
import hashlib
import requests
import time

baseESurl="http://localhost:9200/photodisplayer/photo/"
defaultNote=10
forceAllNote=False
forceAllNoteExcept0=True

def AddPhotoToES(fullPathFile):
	md5file=hashlib.md5(open(fullPathFile, 'rb').read()).hexdigest()
	photoFromES = requests.get("http://localhost:9200/photodisplayer/photo/"+md5file)
	dateFile=time.strftime('%Y-%m-%dT%H:%M:%S', time.gmtime(os.path.getctime(fullPathFile)))
    #2009-11-15T14:12:12
	note=defaultNote
	if forceAllNote or not ("\"found\":true" in photoFromES.text) or (forceAllNoteExcept0 and not ("\"note\": 0" in photoFromES.text)):
	    print( "   inserting :")
	    print( "      "+ fullPathFile)
	    print( "      "+ md5file)
	    print( "      "+ dateFile)
	    print( "      "+ str(note))
	    payload = '{{\"fullpath\": "{0}", "dateFile": "{1}", "note": {2} }}'.format(fullPathFile.replace('\\', '\\\\'),dateFile,str(note))
	    insertRequest = requests.put(baseESurl+md5file, data=payload)
	    print( "      --> " + str(insertRequest.status_code))


try:
    basePathToScan = sys.argv[1]

    if basePathToScan=="" or type(basePathToScan)==type(None):
        raise Exception('My error!')
    else:
        for dossier, sous_dossiers, fichiers in os.walk(basePathToScan):
                for fichier in fichiers:
                    if fichier.lower().endswith(".jpg") or fichier.lower().endswith(".png"):
                        print(dossier+'\\'+fichier)
                        AddPhotoToES(dossier+'\\'+fichier)
except:
    print('Error')
    print("Usage: PhotoCollecteur.py basePathToScan")


