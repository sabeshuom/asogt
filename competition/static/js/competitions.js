function export_competition_details(id) {
    $(id).html("Getting Data ");
    $(id).addClass("loading")
    var xhttp = new XMLHttpRequest();
    var state = $("#competitions_selected_state").text();
    var format = $("#competitions_selected_format").text();
    var year = $("#competitions_selected_year").text();
    var out_ext = ".xlsx";
    var out_fname = "TC_COMPETETION_DETAILS_" + state + "_" + year + "_" + format
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
    xhttp.open("POST", "/asogt/export_competition_details/", true);
    xhttp.setRequestHeader("Content-Type", "application/json");
    xhttp.responseType = 'blob';
    xhttp.send(JSON.stringify({
        'state': state,
        'year': year,
        'format': format
        })
    );
}

function get_competition_details(id) {
    $("#div_competitions").hide()
    $("#competition_main .loading").show();
    var xhttp = new XMLHttpRequest();
    var state = $("#competitions_selected_state").text();
    var year = $("#competitions_selected_year").text();
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
    xhttp.open("POST", "/asogt/get_competition_details/", true);
    xhttp.setRequestHeader("Content-Type", "application/json");
    xhttp.responseType = 'json';
    xhttp.send(JSON.stringify({
        'state': state,
        'year': year,
        })
    );
}

function set_data_table(data){
    if ($.fn.dataTable.isDataTable('#table_competitions')) {
        $('#table_competitions').DataTable().destroy();
    }
    $("#table_competitions .tr-header").html("");

    for(var id in data.headers){
        $("#table_competitions .tr-header").append($("<th>" + data.headers[id] + "</th>"));
    }

    $('#table_competitions').DataTable({
        columns : [{'className': 'hcenter'},{'className': 'hcenter'}, {'className': 'hleft'}, {'className': 'hleft'}, {'className': 'hleft'},{'className': 'hcenter'}],
        responsive: true,
        destroy: true,
        data: data.std_data
    });
    $("#competition_main .loading").hide();
    $("#div_competitions").show()
}

$(document).ready(function() 
{
    $('#app_drop-down').show();
    check_authentication(true)
    get_competition_details();
});