#!/usr/bin/python3
# -*- coding: utf-8 -*


import sys
import os
import hashlib
import requests
import time
import argparse

parser = argparse.ArgumentParser(description='Elastic search Injector for PhotoDisplayer')

parser.add_argument('-f', action="store_true",dest="forceAllNote", default=False, help='force all note to default')
parser.add_argument('-f0', action="store_true",dest="forceAllNoteExcept0", default=False, help='force all note to default except 0')
parser.add_argument('-e', action="store", dest="baseESurl", default="http://localhost:9200/photodisplayer/photo/",  help='ES Url')
parser.add_argument('-d', action="store", dest="directoryToScan", help='Directory to scan for Photo (sub directory included)')
parser.add_argument('-n', action="store", dest="defaultNote", type=int,default=10, help='Default note')
arguments = parser.parse_args()


def AddPhotoToES(fullPathFile):
	md5file=hashlib.md5(open(fullPathFile, 'rb').read()).hexdigest()
	photoFromES = requests.get("http://localhost:9200/photodisplayer/photo/"+md5file)
	dateFile=time.strftime('%Y-%m-%dT%H:%M:%S', time.gmtime(os.path.getctime(fullPathFile)))

	note=arguments.defaultNote
	if arguments.forceAllNote or not ("\"found\":true" in photoFromES.text) or (arguments.forceAllNoteExcept0 and not ("\"note\": 0" in photoFromES.text)):
	    print( "   inserting :")
	    print( "      "+ fullPathFile)
	    print( "      "+ md5file)
	    print( "      "+ dateFile)
	    print( "      "+ str(note))
	    payload = '{{\"fullpath\": "{0}", "dateFile": "{1}", "note": {2} }}'.format(fullPathFile.replace('\\', '\\\\'),dateFile,str(note))
	    insertRequest = requests.put(arguments.baseESurl+md5file, data=payload)
	    print( "      --> " + str(insertRequest.status_code))



basePathToScan = arguments.directoryToScan

if basePathToScan=="" or type(basePathToScan)==type(None):
    raise Exception('My error!')
else:
    for dossier, sous_dossiers, fichiers in os.walk(basePathToScan):
            for fichier in fichiers:
                if fichier.lower().endswith(".jpg") or fichier.lower().endswith(".png"):
                    print(dossier+'\\'+fichier)
                    AddPhotoToES(dossier+'\\'+fichier)


