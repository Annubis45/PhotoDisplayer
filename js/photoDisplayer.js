function SetDim(bloc) {
    console.log(window.innerHeight );
    console.log(document.documentElement.clientWidth);
    document.getElementById(bloc).style.maxHeight = (document.documentElement.clientHeight  ) + "px";
    document.getElementById(bloc).style.maxWidth = document.documentElement.clientWidth+ "px";
}


function SetImage(imageid)
{
    console.log(Date.now() + " --> SetImage : " + imageid);
    currentPhotoMD5=imageid;
    Image3 = new Image();
    Image3.src = "cgi/image.py?idcurrent=" + currentPhotoMD5;
    document.getElementById("image").src = "cgi/image.py?idcurrent=" + currentPhotoMD5;
    console.log(Date.now() + " --> SetImage : END");
}

function Ban() {
    if(currentPhotoMD5==0)
        return;
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function () {
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
            Next();
        }
    }
    xmlhttp.open("GET", "cgi/index.py?action=ban&idcurrent="+currentPhotoMD5, true);
    xmlhttp.send();
}

function Previous() {
    SetImage(PopImageFromBuffer());
}

function Next() {
    console.log(Date.now() + " --> Next ");
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function () {
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
            var imageid=xmlhttp.responseText;
            SetImage(imageid);
            AddImageInBuffer(imageid)
            console.log(Date.now() + " --> " + xmlhttp.responseText);
        }
    }
    xmlhttp.open("GET", "cgi/index.py?action=next", true);
    xmlhttp.send();
    console.log(Date.now() + " --> Next : END");
}

function Like() {
    if(currentPhotoMD5==0)
        return;

    var xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function () {
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
            //document.getElementById("myDiv").innerHTML=xmlhttp.responseText;
        }
    }
    xmlhttp.open("GET", "cgi/index.py?action=like&idcurrent="+currentPhotoMD5, true);
    xmlhttp.send();
}

function Dislike() {
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function () {
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
            //document.getElementById("myDiv").innerHTML=xmlhttp.responseText;
        }
    }
    xmlhttp.open("GET", "cgi/index.py?action=dislike&idcurrent="+currentPhotoMD5, true);
    xmlhttp.send();
}

function Init(RefreshTime) {
    window.onload = function () { SetDim("image") };
    window.onresize = function () { SetDim("image") };
    window.setInterval("Next()", RefreshTime);
    Next();
    window.scrollTo(0, 1);
}

function AddImageInBuffer(image)
{
    imagesBufferPosition=(imagesBufferPosition+1)%imagesBufferSize;
    imageBuffer[imagesBufferPosition]=image;
}

function PopImageFromBuffer()
{
    imagesBufferPosition=(imagesBufferPosition-1)%imagesBufferSize;
    return imageBuffer[imagesBufferPosition];
}

var currentPhotoMD5=0;
var imagesBufferPosition=-1;
var imageBuffer = new Array();
var imagesBufferSize=30;
var RefreshTime=1000*15;
Init(RefreshTime);



