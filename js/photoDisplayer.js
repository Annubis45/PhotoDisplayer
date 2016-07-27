function SetDim(bloc) {
    var hauteur;
    var largeur;

    if (typeof (window.innerWidth) == 'number')
        hauteur = window.innerHeight;
    else if (document.documentElement && document.documentElement.clientHeight)
        hauteur = document.documentElement.clientHeight;

    if (typeof (window.innerHeight) == 'number')
        largeur = window.innerWidth;
    else if (document.documentElement && document.documentElement.clientWidth)
        largeur = document.documentElement.clientWidth;

    if (largeur / hauteur > 1.5) {
        document.getElementById(bloc).style.height = (hauteur - 0) + "px";
        document.getElementById(bloc).style.width = "auto";
    }
    else {
        document.getElementById(bloc).style.width = (largeur - 0) + "px";
        document.getElementById(bloc).style.height = "auto";
    }
}


function SetImage(imageid)
{
    currentPhotoMD5=imageid;
    Image3 = new Image();
    Image3.src = "cgi/image.py?idcurrent=" + currentPhotoMD5;
    document.getElementById("image").src = "cgi/image.py?idcurrent=" + currentPhotoMD5;
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
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function () {
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
            var imageid=xmlhttp.responseText;
            SetImage(imageid);
            AddImageInBuffer(imageid)
            console.log(xmlhttp.responseText);
        }
    }
    xmlhttp.open("GET", "cgi/index.py?action=next", true);
    xmlhttp.send();
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
    xmlhttp.open("GET", "cgi/index.py?action=dislike&idcurrent=", true);
    xmlhttp.send();
}

function Init() {
    window.onload = function () { SetDim("image") };
    window.onresize = function () { SetDim("image") };
    window.setInterval("Next()", 5000);
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
Init();