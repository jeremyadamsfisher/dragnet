$(document).ready(function(){
    /* https://stackoverflow.com/questions/10333971/html5-pre-resize-images-before-uploading */

    const formField = document.getElementById("files");
    const progress = document.getElementById("uploadProgress");
    function showUploader() {
        formField.style.display = "none";
        progress.style.display = "inline-block";
    }

    $("form#files").submit(function(e) {
        e.preventDefault();
        showUploader();

        const img = document.createElement("img");
        const canvas = document.createElement("canvas");
        const reader = new FileReader();  
        reader.onload = function(e) {
            img.src = e.target.result;

            canvas.getContext("2d").drawImage(img, 0, 0);

            const maxSize = 512;
            let width = img.width;
            let height = img.height;
            if (maxSize <= width || maxSize <= height) {
                if (width > height) {
                    if (width > maxSize) {
                        height *= maxSize / width;
                        width = maxSize;
                    }
                } else {
                    if (height > maxSize) {
                        width *= maxSize / height;
                        height = maxSize;
                    }
                }
            }
            canvas.width = width;
            canvas.height = height;

            canvas.getContext("2d").drawImage(img, 0, 0, width, height);

            $.ajax({
                url: "/enqueue",
                type: "POST",
                data : canvas.toDataURL("image/jpeg"),
                success: function (response) {
                    setTimeout(function(){
                        if (response.result === "failure") {
                            alert("Error with uploaded image!");
                            window.location.replace("/");
                        } else if (response.result === "success") {
                            window.location.replace(response.result_page);
                        }
                    }, 1000);
                },
            });
        }
        const filesToUpload = document.getElementById("fileChooser").files;
        reader.readAsDataURL(filesToUpload[0]);
    });
}); 