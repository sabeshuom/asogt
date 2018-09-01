function get_student_details(id) {
    $(id).addClass("loading")
    var xhttp = new XMLHttpRequest();
    var state = $("#students_selected_state").text();
    var format = $("#students_selected_format").text();
    var year = $("#students_selected_year").text();

    var xls_file_name = "TC_STUDENT_DETAILS_" + state + "_" + year + "_" + format
    xhttp.onreadystatechange = function () {
        var a, today;
        if (xhttp.readyState === 4) {
            if (xhttp.status === 200) {
                a = document.createElement('a');
                a.href = window.URL.createObjectURL(xhttp.response);
                today = new Date();
                a.download = xls_file_name + "_" + today.toDateString().split(" ").join("_") + ".xlsx";
                a.style.display = 'none';
                document.body.appendChild(a);
                $(id).removeClass("loading");
                return a.click();
            }
            else {
                $(id).removeClass("loading");
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
    $(id).addClass("loading")
    var xhttp = new XMLHttpRequest();
    var state = $("#results_selected_state").text();
    var format = $("#results_selected_format").text();
    var year = $("#results_selected_year").text();

    // var state = $(id).attr("data-state");
    // var year = $(id).attr("data-year");
    // var format = $(id).attr("data-format");
    var xls_file_name = "TC_RESULTS_" + state + "_" + year + "_" + format
    xhttp.onreadystatechange = function () {
        var a, today;
        if (xhttp.readyState === 4) {
            if (xhttp.status === 200) {
                a = document.createElement('a');
                a.href = window.URL.createObjectURL(xhttp.response);
                today = new Date();
                a.download = xls_file_name + "_" + today.toDateString().split(" ").join("_") + ".xlsx";
                a.style.display = 'none';
                document.body.appendChild(a);
                $(id).removeClass("loading");
                return a.click();
            }
            else {
                $(id).removeClass("loading");
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