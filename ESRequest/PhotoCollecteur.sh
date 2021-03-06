#!/bin/bash

baseESurl="http://localhost:9200/photodisplayer/photo/"
basePath="."
OIFS="$IFS"
IFS="
"
for m in `find $basePath -type f -iname "*.JPG" ! -path "*PRIVATE*" ! -path "*private*"` ; do
	echo $m
	md5file=$(md5sum ${m}  | awk '{print $1}' );
	askES=$(curl -XGET "$baseESurl""$md5file");
	fullpath=$(readlink -f $m);
	dateFile=$(date +"%d/%m/%y %T" -r ${m});
	note=10;

	if ! [[ "$askES" == *"\"found\":true"* ]];
	then
		echo "   inserting :"
		echo "       $fullpath"
		echo "       $md5file"
		echo "       $dateFile"
		echo "       $note"
	   	curl -XPUT "$baseESurl""$md5file" -d "{
		\"fullpath\": \"$fullpath\",
		\"dateFile\":\"$dateFile\",
		\"note\": $note,
		\"id\":\"$md5file\"
		}"

	fi

done;
	
IFS="$OIFS"


#curl -XPUT 'http://localhost:9200/photodisplayer/photo/1' -d'{
#"info": "test1",
#"md5":"rtgfythhygfhh",
#"note": 10,
#"path":"/media/data/photo/photo1.jpg"
#}'


#curl -XGET 'http://localhost:9200/photodisplayer/photo/AU8X3WxxH88PT0fMWVzn'
