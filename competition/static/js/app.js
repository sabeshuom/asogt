function get_student_details(id) {
    $(id).html("Processing ...");
    $(id).addClass("loading")
    var xhttp = new XMLHttpRequest();
    var state = $("#students_selected_state").text();
    var format = $("#students_selected_format").text();
    var year = $("#students_selected_year").text();
    var out_ext = ".xlsx";
    var out_fname = "TC_STUDENT_DETAILS_" + state + "_" + year + "_" + format
    xhttp.onreadystatechange = function () {
        var a, today;
        if (xhttp.readyState === 4) {
            if (xhttp.status === 200) {
                $(id).html("Download");
                $(id).removeClass("loading");
                a = document.createElement('a');
                a.href = window.URL.createObjectURL(xhttp.response);
                today = new Date();
                a.download = out_fname + "_" + today.toDateString().split(" ").join("_") + out_ext;
                a.style.display = 'none';
                document.body.appendChild(a);
                return a.click();
            }
            else {
                alert("Something went wrong.Please check with Admin.")
            }
        }
    };
    xhttp.open("POST", "/asogt/get_student_details/", true);
    xhttp.setRequestHeader("Content-Type", "application/json");
    xhttp.responseType = 'blob';
    xhttp.send(JSON.stringify({
        'state': state,
        'year': year,
        'format': format
        })
    );
}

function get_results(id) {
    $(id).html("Processing ...");
    $(id).addClass("loading")
    var xhttp = new XMLHttpRequest();
    var state = $("#results_selected_state").text();
    var format = $("#results_selected_format").text();
    var year = $("#results_selected_year").text();
    var out_ext = ".xlsx";
    if(format=="Book Word"){
        out_ext = ".docx"
    }
    var out_fname = "TC_RESULTS_" + state + "_" + year + "_" + format
    xhttp.onreadystatechange = function () {
        var a, today;
        if (xhttp.readyState === 4) {
            $(id).removeClass("loading");
            $(id).html("Download");
            if (xhttp.status === 200) {
                a = document.createElement('a');
                a.href = window.URL.createObjectURL(xhttp.response);
                today = new Date();
                a.download = out_fname + "_" + today.toDateString().split(" ").join("_") + out_ext;
                a.style.display = 'none';
                document.body.appendChild(a);
                return a.click();
            }
            else {
                alert("Something went wrong.Please check with Admin.")
            }
        }
    };
    xhttp.open("POST", "/asogt/get_results/", true);
    xhttp.setRequestHeader("Content-Type", "application/json");
    xhttp.responseType = 'blob';
    xhttp.send(JSON.stringify({
        'state': state,
        'year': year,
        'format': format
        })
    );
}

$(document).ready(function() {
  $('#popup-login').on('hidden.bs.modal', function (e) {
        check_authentication(true);
  });

});