$(document).ready(function(){
    /* https://stackoverflow.com/questions/10333971/html5-pre-resize-images-before-uploading */

    $("form#files").submit(function(e) {
        e.preventDefault();

        var filesToUpload = document.getElementById("fileChooser").files;
        var file = filesToUpload[0];

        var canvas = document.createElement("canvas");

        var img = document.createElement("img");
        var reader = new FileReader();  
        reader.onload = function(e) {img.src = e.target.result}
        reader.readAsDataURL(file);

        var ctx = canvas.getContext("2d");
        ctx.drawImage(img, 0, 0);
        var MAX_WIDTH = 800;
        var MAX_HEIGHT = 600;
        var width = img.width;
        var height = img.height;
        if (width > height) {
            if (width > MAX_WIDTH) {
                height *= MAX_WIDTH / width;
                width = MAX_WIDTH;
            }
        } else {
            if (height > MAX_HEIGHT) {
                width *= MAX_HEIGHT / height;
                height = MAX_HEIGHT;
            }
        }
        canvas.width = width;
        canvas.height = height;
        var ctx = canvas.getContext("2d");
        ctx.drawImage(img, 0, 0, width, height);

        var dataurl = canvas.toDataURL("image/png");
        /*document.getElementById("fileChooser").files[0]= dataurl;*/

        /* update interface */
        var formField = document.getElementById("files");
        var progress = document.getElementById("uploadProgress");
        setTimeout(function(){
            formField.style.display = "none";
            progress.style.display = "inline-block";
        }, 1000)

        /* var formData = new FormData(this); */

        $.ajax({
            url: "/enqueue",
            type: 'POST',
            img : dataurl,
            success: function (data) {
                setTimeout(function(){
                    window.location.replace(data.result_page);
                }, 5000);
            },
            cache: false,
            contentType: false,
            processData: false
        });
    });
}); 