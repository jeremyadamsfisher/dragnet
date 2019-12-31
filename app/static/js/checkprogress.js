"use strict";

function showDrag(imgUrl) {
    // hide loader
    let loaderView = document.getElementById("loader");
    loaderView.style.display = "none";

    // update tag line
    let tagLine = document.getElementById("tagLine").getAttribute("tagLine");
    document.getElementById("subtitle").innerHTML = tagLine;

    // show drag image
    let imgTarget = document.getElementById("imgTarget");
    imgTarget.src = imgUrl;
    imgTarget.style.display = "inline-block";
};

function showError(err) {
    // make this better 
    alert(`Error: ${err}`);
};

function pingBackendForImage(imgId, n) {
    if (n === 0) {
        showError("time out!");
    } else {
        fetch(`/checkprogress/${imgId}`)
            .then(response => response.json())
            .then(j => {
                if (j.status === "loading") {
                    setTimeout(() => pingBackendForImage(imgId, n-1), 1000);
                } else if (j.status === "done") {
                    showDrag(j.url);
                }
            })
            .catch(err => showError(err));
    }
};

function init() {
    let elements = location.href.split("/");
    let imgId = elements[elements.length - 1];
    pingBackendForImage(imgId, 5);
};