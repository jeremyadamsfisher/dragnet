"use strict";

function toggleView(view) {
	const formFieldView = document.getElementById("filesView");
    const progressView = document.getElementById("uploadProgressView");
    const resultView = document.getElementById("resultsView")

	if (view === "default") {
		formFieldView.style.display = "inline-block";
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

function setDragImgSrc(src) {
	const dragImg = document.getElementById("resultImg");
	dragImg.src = src;
}

function showError(err) {
    // todo: make this better
    alert(`Error: ${err}`);
}

function setUpFileForm() {
    const fileForm = document.getElementById("filesView");

    const enqueueUrl = document.getElementById("enqueueUrl")
    	.getAttribute("enqueueurl");
    const loadingLine = document.getElementById("loadingLine")
    	.getAttribute("loadingline");
    const loadedLine = document.getElementById("loadedLine")
    	.getAttribute("loadedline")

    fileForm.onsubmit = (event) => {
        event.preventDefault();

        setMessage(loadingLine);
        toggleView("uploading");

        const img = document.getElementById("fileChooser").files[0];
        fetch(enqueueUrl, {method: "POST", body: img})
            .then(response => response.json())
            .then(j => {
            	setMessage(loadedLine);
            	toggleView("predicting");
            	pingBackendForImage(j.img_id, 30);
			})
            .catch(err => {
            	toggleView("default");
                showError(err);
            })
    };
}

function pingBackendForImage(imgId, n) {
    if (n === 0) {
        throw new Error("time out!");
    } else {
    	const url = document.getElementById("checkProgressUrl")
    		.getAttribute("checkprogressurl");
        fetch(url + imgId)
            .then(response => response.json())
            .then(j => {
                if (j.status === "loading") {
                    setTimeout(() => pingBackendForImage(imgId, n-1), 1000);
                } else if (j.status === "done") {
                    showDrag(j.url);
                }
            });
    }
}