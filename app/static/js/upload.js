"use strict";

function showFileForm(_showFileForm) {
    let formField = document.getElementById("files");
    let progress = document.getElementById("uploadProgress");
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

function setUpFileForm() {
    let fileForm = document.getElementById("files");
    fileForm.onsubmit = (event) => {
        event.preventDefault();
        showFileForm(true);
        let img = document.getElementById("fileChooser").files[0];
        fetch("/enqueue", {method: "POST", body: img})
            .then(response => response.json())
            .then(j => window.location.replace(j.result))
            .catch(err => {
                showError(err);
                showFileForm(false);
            });
    };
};

window.onload = () => {
    setUpFileForm();
};