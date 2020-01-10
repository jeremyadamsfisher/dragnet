"use strict";

let quipUrl, enqueueUrl, saveToGalleryUrl;

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

function setDragImgSrc(src, imgID) {
	document.getElementById("resultImg").src = src;
    document.getElementById("uploadBtn").onclick = () => {
        fetch(saveToGalleryUrl + imgID);
        showInfo("Thanks for your submission! I'll review it and consider whether to include it in the gallery - Jeremy", "info");
    };
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

function showError(err) {
    showInfo(err.message, "error");
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

function predict(imgFile) {
    const loadingViewLabel = document.getElementById("uploadProgressViewLabel");
    const resultsViewLabel = document.getElementById("resultsViewLabel");

    getQuip("uploading", quip => { loadingViewLabel.innerHTML = quip; });
    toggleView("uploading");

    fetch(enqueueUrl, {method: "POST", body: imgFile})
        .then(response => response.json())
        .then(j => {
            getQuip("predicting", quip => { loadingViewLabel.innerHTML = quip; });
            const imgId = j.img_id;
            const checkProgressUrl = j.result;
            pingBackendForImage(checkProgressUrl, 50, (resultUrl) => {
                setDragImgSrc(resultUrl, imgId);
                getQuip("done", quip => { resultsViewLabel.innerHTML = quip; });
                toggleView("result");
            });

        })
        .catch(err => {
            toggleView("default");
            showError(err);
        });
}

function setUpDropZone() {
    new Dropzone("#dragzone", {
         url: enqueueUrl,
         createImageThumbnails: false,
         init: function() {
            this.on("addedfile", imgFile => { predict(imgFile); });
            this.on("complete", () => { this.removeAllFiles(); });
        }
    });
}

function getQuip(quipType, callback) {
    fetch(quipUrl + quipType)
        .then(resp => resp.json())
        .then(j => { callback(j.quip); });
}

function init(_quipUrl, _enqueueUrl, _saveToGalleryUrl) {
    quipUrl = _quipUrl;
    enqueueUrl = _enqueueUrl;
    saveToGalleryUrl = _saveToGalleryUrl;
    setUpDropZone();
}