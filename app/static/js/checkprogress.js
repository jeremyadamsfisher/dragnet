'use strict';
$(document).ready(function(){
    const imgId = document.getElementById("imgId").getAttribute("imgId");
    const tagLine = document.getElementById("tagLine").getAttribute("tagLine");

    const uri = "https://storage.googleapis.com/dragnet_imgs/" + imgId;
    function showDrag() {
        let imgTarget = document.getElementById("imgTarget");
        imgTarget.src = uri;
        imgTarget.style.display = "inline-block";
        document.getElementById("subtitle").innerHTML = tagLine;
        document.getElementById("loader").style.display = "none";
    }
    function showError() {
        document.getElementById("subtitle").innerHTML = "error! (please try again.)";
        document.getElementById("loader").style.display = "none";
    }
    function pingGcp(n){
        if (n === 0) {
            showError();
        } else {
            let http = new XMLHttpRequest();
            http.open("HEAD", "https://cors-anywhere.herokuapp.com/" + uri, false);
            http.onload = (e) => {
                if (http.status === 404) {
                    setTimeout( function() { pingGcp(n-1); }, 5000);
                } else {
                    showDrag();
                }
            }
            http.send();
        }
    }
    pingGcp(5);
}); 