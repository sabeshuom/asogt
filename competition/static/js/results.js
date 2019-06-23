function export_results(id) {
    $(id).find("p").show()
    $(id + " i").hide()
    $(id).addClass("loading")
    var xhttp = new XMLHttpRequest();
    var state = $("#results_selected_state").text();
    var format = $(id).data().type;
    var year = $("#results_selected_year").text();
    var out_ext = ".xlsx";
    if(format=="book word"){
        out_ext = ".docx"
    }
    var out_fname = "TC_RESULTS_" + state + "_" + year + "_" + format
    xhttp.onreadystatechange = function () {
        var a, today;
        if (xhttp.readyState === 4) {
            $(id).removeClass("loading");
            $(id + " p").hide()
            $(id + " i").show()
            // $(id).html("<i class='fa fa-file-export'></i>");
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
    xhttp.open("POST", "/asogt/export_results/", true);
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
    $("#div_results").hide()
    $("#result_main .loading").show();
    var xhttp = new XMLHttpRequest();
    var state = $("#results_selected_state").text();
    var year = $("#results_selected_year").text();
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
    xhttp.open("POST", "/asogt/get_results/", true);
    xhttp.setRequestHeader("Content-Type", "application/json");
    xhttp.responseType = 'json';
    xhttp.send(JSON.stringify({
        'state': state,
        'year': year,
        })
    );
}

function set_data_table(data){
    if ($.fn.dataTable.isDataTable('#table_results')) {
        $('#table_results').DataTable().destroy();
    }
    $("#table_results .tr-header").html("");

    for(var id in data.headers){
        $("#table_results .tr-header").append($("<th>" + data.headers[id] + "</th>"));
    }

    $('#table_results').DataTable({
        //headers = ["StdNo", "Name (T)", "Name (E)", 'Exam', "Competition", 'Grade', 'Award']
        columns : [{'className': 'hcenter'},{'className': 'hleft'}, {'className': 'hleft'}, {'className': 'hleft'}, {'className': 'hleft'},{'className': 'hcenter'}, {'className': 'hcenter'}],
        responsive: true,
        destroy: true,
        data: data.result_data
    });
    $("#result_main .loading").hide();
    $("#div_results").show()
}

$(document).ready(function() 
{
    $('#app_drop-down').show();
    check_authentication(true)
    get_results();
});