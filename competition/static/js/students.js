function export_student_details(id) {
    $(id).html("Compiling xlx");
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
                $(id).html("<i class='fa fa-file-export'></i>");
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
    xhttp.open("POST", "/asogt/export_student_details/", true);
    xhttp.setRequestHeader("Content-Type", "application/json");
    xhttp.responseType = 'blob';
    xhttp.send(JSON.stringify({
        'state': state,
        'year': year,
        'format': format
        })
    );
}

function get_student_details(id) {
    $("#div_students").hide()
    $("#student_main .loading").show();
    var xhttp = new XMLHttpRequest();
    var state = $("#students_selected_state").text();
    var year = $("#students_selected_year").text();
    xhttp.onreadystatechange = function () {
        var a, today;
        if (xhttp.readyState === 4) {
            if (xhttp.status === 200) {
                var data = xhttp.response;
                set_data_table(data)
            }
            else {
                alert("Something went wrong.Please check with Admin.")
            }
        }
    };
    xhttp.open("POST", "/asogt/get_student_details/", true);
    xhttp.setRequestHeader("Content-Type", "application/json");
    xhttp.responseType = 'json';
    xhttp.send(JSON.stringify({
        'state': state,
        'year': year,
        })
    );
}

function set_data_table(data){
    if ($.fn.dataTable.isDataTable('#table_students')) {
        $('#table_students').DataTable().destroy();
    }
    $("#table_students .tr-header").html("");

    for(var id in data.headers){
        $("#table_students .tr-header").append($("<th>" + data.headers[id] + "</th>"));
    }

    $('#table_students').DataTable({
        columns : [{'className': 'hcenter'},{'className': 'hcenter'}, {'className': 'hleft'}, {'className': 'hleft'}, {'className': 'hleft'},{'className': 'hleft'}, {'className': 'hleft'},{'className': 'hleft'},{'className': 'hleft'}],
        responsive: true,
        destroy: true,
        data: data.students_data
    });
    $("#student_main .loading").hide();
    $("#div_students").show()
}

$(document).ready(function() 
{
    $('#app_drop-down').show();
    check_authentication(true)
    get_student_details();
});