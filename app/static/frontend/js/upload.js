"use strict";

function showFileForm(_showFileForm) {
    const formField = document.getElementById("files");
    const progress = document.getElementById("uploadProgress");
    if (_showFileForm) {
        formField.style.display = "none";
        progress.style.display = "inline-block";
    } else {
        formField.style.display = "inline-block";
        progress.style.display = "none";
    }
};

function showError(err) {
    // todo: make this better
    alert(`Error: ${err}`);
}

function showMessageOnUploadScreen(msg) {

}

function setUpFileForm() {
    const fileForm = document.getElementById("files");
    const enqueueUrl = document.getElementById("enqueueUrl").getAttribute("enqueueurl");
    fileForm.onsubmit = (event) => {
        event.preventDefault();
        showFileForm(true);
        const img = document.getElementById("fileChooser").files[0];
        fetch(enqueueUrl, {method: "POST", body: img})
            .then(response => response.json())
            .then(j => {
            	alert(j.result);
			})
            .catch(err => {
                showError(err);
                showFileForm(false);
            })
    };
};