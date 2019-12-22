'use strict';
$(document).ready(function(){
    const imgId = document.getElementById("imgId").getAttribute("img_id");
    const tagLine = document.getElementById("tagLine").getAttribute("tag_line");
    const url = "https://storage.googleapis.com/dragnet_imgs/" + imgId;
    
    function showDrag() {
        let imgTarget = document.getElementById("imgTarget");
        imgTarget.src = "https://cors-anywhere.herokuapp.com/" + url;
        imgTarget.style.display = "inline-block";
        document.getElementById("subtitle").innerHTML = tagLine;
        hideLoader();
    }
    function showError() {
        document.getElementById("subtitle").innerHTML = "error! (please try again later.)";
        hideLoader();
    }
    function hideLoader() {
        document.getElementById("loader").style.display = "none";
    }
    function pingDone(n) {
        if (n === 0) {
            showError();
        } else {
            $.ajax({
                url: "/checkprogress/" + imgId,
                type: "GET",
                success: function (response) {
                    console.log(response);
                    if (response.drag_status === "loading") {
                        setTimeout( function() { pingDone(n-1); }, 5000);
                    } else if (response.drag_status === "done") {
                        showDrag();
                    }
                },
            });
        }
    }
    pingDone(5);
}); 