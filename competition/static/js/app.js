function get_per_exam_details(id) {
    $(id).addClass("loading")
    var xhttp = new XMLHttpRequest();
    var state = $(id).attr("data-state");
    var xls_file_name = "TC_StudentList_2018_" + state + "2018"
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
                $('#popup-login').modal('show');
            }
        }
    };
    xhttp.open("POST", "/asogt/get_per_exam_details/", true);
    xhttp.setRequestHeader("Content-Type", "application/json");
    xhttp.responseType = 'blob';
    xhttp.send(JSON.stringify({
        'state': state,
        })
    );
}

function get_resuls_for_certificate(id) {
    $(id).addClass("loading")
    var xhttp = new XMLHttpRequest();
    var state = $(id).attr("data-state");
    var xls_file_name = "TC_RESULTS_2018_" + state + "2018_for_certificate"
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
                $('#popup-login').modal('show');
            }
        }
    };
    xhttp.open("POST", "/asogt/get_results_for_certificate/", true);
    xhttp.setRequestHeader("Content-Type", "application/json");
    xhttp.responseType = 'blob';
    xhttp.send(JSON.stringify({
        'state': state,
        })
    );
}

// $(document).ready(function() {
//   $('#popup-login').on('hidden.bs.modal', function (e) {
//       if($("#a-login").html().toLowerCase() == "login"){
//           window.location.href = "/";
//       }
//   });

// });