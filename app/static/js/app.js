"use strict";

function toggleView(view) {
	const formFieldView = document.getElementById("dragzone");
    const progressView = document.getElementById("uploadProgressView");
    const resultView = document.getElementById("resultsView")

	if (view === "default") {
		formFieldView.style.display = "block";
        progressView.style.display = "none";
        resultView.style.display = "none";
	} else if (view === "uploading" || view === "predicting") {
		formFieldView.style.display = "none";
        progressView.style.display = "inline-block";
        resultView.style.display = "none";
	} else if (view === "result") {
		formFieldView.style.display = "none";
        progressView.style.display = "none";
        resultView.style.display = "inline-block";
	} else {
		throw new Error(`unknown view: ${view}`);
	}
}

function setMessage(msg) {
	document.getElementById("uploadProgressViewLabel").innerHTML = msg;
	document.getElementById("resultsViewLabel").innerHTML = msg;
}

function setDragImgSrc(src, imgID) {
    const uploadToGalleryUrl = document.getElementById("galleryUrl")
        .getAttribute("galleryurl");
	document.getElementById("resultImg").src = src;
    document.getElementById("uploadBtn").onclick = () => {
        fetch(uploadToGalleryUrl + imgID);
        showInfo("Thanks for your submission! I'll review it and consider whether to include it in the gallery - Jeremy", "info");
    };
}

function showError(err) {
    showInfo(err.message, "error");
}

function showInfo(msg, infoType) {
    const messagePanel = document.getElementById("messagePanel");
    if (infoType === "error") {
        messagePanel.classList.add("message-panel-error");
        messagePanel.classList.remove("message-panel-info");
    } else {
        messagePanel.classList.add("message-panel-info");
        messagePanel.classList.remove("message-panel-error");
    }
    messagePanel.style.display = "block";
    messagePanel.innerHTML = msg;
    messagePanel.scrollIntoView(); 
}

function pingBackendForImage(url, n, callback) {
    if (n === 0) {
        toggleView("default");
		showError("time out!");
    } else {
        fetch(url)
            .then(response => response.json())
            .then(j => {
                if (j.status === "loading") {
                    setTimeout(() => pingBackendForImage(url, n-1, callback), 1000);
                } else if (j.status === "done") {
                	callback(j.url);
                } else {
                	throw new Error("invalid response");
                }
            });
    }
}

function upload(img_file) {
    const enqueueUrl = document.getElementById("enqueueUrl")
    	.getAttribute("enqueueurl");
    const loadingLine = document.getElementById("loadingLine")
    	.getAttribute("loadingline");
    const loadedLine = document.getElementById("loadedLine")
        .getAttribute("loadedline");
    
    setMessage(loadingLine);
    toggleView("uploading");

    fetch(enqueueUrl, {method: "POST", body: img_file})
        .then(response => response.json())
        .then(j => {
            setMessage("still shantaying...");
            const imgId = j.img_id;
            const checkProgressUrl = j.result;
            pingBackendForImage(checkProgressUrl, 50, (resultUrl) => {
                setDragImgSrc(resultUrl, imgId);
                setMessage(loadedLine);
                toggleView("result");
            });

        })
        .catch(err => {
            toggleView("default");
            showError(err);
        });
}

function setUpDropZone() {
    const enqueueUrl = document
        .getElementById("enqueueUrl")
        .getAttribute("enqueueurl");
    const dropZone = new Dropzone("#dragzone", {
         url: enqueueUrl,
         createImageThumbnails: false,
         init: function() {
            this.on("addedfile", file => { upload(file); });
            this.on("complete", file => { this.removeAllFiles(); });
        }
    });
}

function init() {
    setUpDropZone();
}