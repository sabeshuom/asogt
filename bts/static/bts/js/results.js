var SEAT_NO_MAP = {};
$(document).ready(function() {
    document.querySelector("html").classList.add('js');

    var fileInput  = document.querySelector(".input-file");
    var the_return = document.querySelector(".file-return");
        
    // button.addEventListener( "keydown", function( event ) {  
    //     if ( event.keyCode == 13 || event.keyCode == 32 ) {  
    //         fileInput.focus();  
    //     }  
    // });
    // button.addEventListener( "click", function( event ) {
    // fileInput.focus();
    // return false;
    // });  
    fileInput.addEventListener( "change", function( event ) {  
        the_return.innerHTML = this.value;  
        handleFileSelect(event);
    }); 
});

function excelToJSON(file) {
    var reader = new FileReader();
 
    reader.onload = function (e) {
        var data = e.target.result;
        var workbook = XLSX.read(data, {
            type: 'binary'
        });
        var XL_row_object = XLSX.utils.sheet_to_row_object_array(workbook.Sheets["Trophy_template"], { range: 5 });
        for (row in XL_row_object) {
            var std_no = XL_row_object[row]['Std No'];
            var seat_no = XL_row_object[row]['Seat No'];
            SEAT_NO_MAP[std_no] = seat_no;
        }
    };

    reader.onerror = function (ex) {
        console.log(ex);
    };

    reader.readAsBinaryString(file);

};

function handleFileSelect(evt) {
    var files = evt.target.files; // FileList object
    excelToJSON(files[0]);
}

function export_results(id) {
    $(id).find("p").show()
    $(id + " i").hide()
    $(id).addClass("loading")
    var xhttp = new XMLHttpRequest();
    var state = $("#results_selected_state").text();
    var format = $(id).data().type;
    var year = $("#results_selected_year").text();
    var out_ext = ".xlsx";
    var gen_seat_no =  $("#gen-seatno").is(':checked');
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
        'format': format,
        'gen_seat_no': gen_seat_no,
        'seat_no_map': SEAT_NO_MAP,
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
    $("#result_main .loading").hide();
    // get_results();
    $("#gen-seatno").change(function(){
        if($(this).is(':checked')) {
            $("#div-input").hide()
            // Checkbox is checked..
        } else {
            $("#div-input").show()
            // Checkbox is not checked..
        }
    });
});