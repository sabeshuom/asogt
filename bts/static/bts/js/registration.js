//jQuery time
var current_fs, next_fs, previous_fs; //fieldsets
var validator;
var student_id = 0;
var year = 2020;
function do_validation(page) {
    var is_valid = true;
    // var page_elements = $("." + current_fs[0].id);
    $("." + page).each(function () {
        if (validator.element(this) == false) {
            is_valid = false;
        }
    });
    return is_valid
}

// function onLoad() {
//     var options = {
//       sourceLanguage: 'en', 
//       destinationLanguage:  ['gu', 'ml', 'hi', 'kn', 'ta', 'te'],
//       shortcutKey: 'ctrl+m',
//       transliterationEnabled: true
//     }
//     // Create an instance on TransliterationControl with the required options.
//     var control = new google.elements.transliteration.TransliterationControl(options);

//     // Enable transliteration in the textfields with the given ids.
//     var ids = [];
//     $("." + tamil).each(function() {
//             ids.push(this.id)
//       });
//     control.makeTransliteratable(ids);
//     // Show the transliteration control which can be used to toggle between English and Hindi and also choose other destination language.
//     // control.showControl('translControl');
//   }


google.load("elements", "1", {
    packages: "transliteration"
});
tamil_ids = []

function onLoad() {
    var options = {
        sourceLanguage:
            google.elements.transliteration.LanguageCode.ENGLISH,
        destinationLanguage:
            [google.elements.transliteration.LanguageCode.TAMIL],
        shortcutKey: 'ctrl+g',
        transliterationEnabled: true
    };
    var control =
        new google.elements.transliteration.TransliterationControl(options);

    control.makeTransliteratable(tamil_ids);
}

function show_popup_alert(alert_title, alert_disc, confirm_but_data) {
    if (confirm_but_data == '')
        confirm_but_data = "info";
    if (confirm_but_data == 'info')
        $("#SB_poup_confirm").css({ 'display': "none" })
    else if (confirm_but_data.hasOwnProperty("callback")) {
        $("#SB_poup_confirm").css({ 'display': "" });
        document.getElementById("SB_but_popup_confirm").setAttribute("onClick", confirm_but_data.callback);
    }
    $("#SB_alert_title").html(alert_title);
    $("#SB_alert_disc").html(alert_disc);
    $('#SB_popup_alert').modal({
        show: 'true'
    });

}

$('#SB_popup_alert').on('hidden.bs.modal', function () {
    location.reload();
})

function add_click_events() {

    $(".next").click(function () {
        current_fs = $(this).parent();
        next_fs = $(this).parent().next();
        var page = current_fs[0].id;
        is_valid = do_validation(page);
        if (is_valid) {
            //activate next step on progressbar using the index of next_fs
            $("#progressbar li").eq($("fieldset").index(next_fs)).addClass("active");
            //show the next fieldset
            next_fs.show();
            current_fs.hide();
        }
    });

    $(".previous").click(function () {
        current_fs = $(this).parent();
        previous_fs = $(this).parent().prev();

        //de-activate current step on progressbar
        $("#progressbar li").eq($("fieldset").index(current_fs)).removeClass("active");

        //show the previous fieldset
        previous_fs.show();
        //hide the current fieldset with style
        current_fs.hide();

    });

    $(".addstudent").click(function () {
        current_fs = $(this).parent();
        var page = current_fs[0].id;
        if (do_validation(page)) {
            $(".addstudent").remove();
            $(".delstudent").remove();
            $(".previous").remove();
            $(".next").remove();
            add_student_page();
        }
    });
    $(".delstudent").click(function () {
        $("#student_" + student_id).remove();
        student_id -= 1;
        if (student_id < 2) {
            $(".delstudent").remove();
        }
    });
}


function add_parent_fields(parent_id, title, page) {
    var div_html = '\
    <h3>' + title + '</h3>\
    <p class="form-label"><label for="'+ parent_id + '_title"> Title </label></p>\
    <span class="select-wrapper">\
    <select id="'+ parent_id + '_title" class="' + page + '" name="' + parent_id + '_title" tabindex="0">\
    <option value="Dr.">Dr.</option>\
    <option value="Mr." selected>Mr.</option>\
    <option value="Mrs.">Mrs.</option>\
    <option value="" selected></option>\
    </select>\
    </span>\
    <p class="form-label"><label for="'+ parent_id + '_surname">Surname </label></p>\
    <input id="'+ parent_id + '_surname"  class="' + page + '" name="' + parent_id + '_surname" placeholder="Surname" tabindex="1" type="text">\
    <p class="form-label"><label for="'+ parent_id + '_givenname">Given Name </label></p>\
    <input id="'+ parent_id + '_givenname"  class="' + page + '" name="' + parent_id + '_givenname" placeholder="Given Name" tabindex="3" type="text">\
    <p class="form-label"><label for="'+ parent_id + '_tel_home">Telephone (Home) </label></p>\
    <input id="'+ parent_id + '_tel_home"  class="' + page + '" name="' + parent_id + '_tel_home"  placeholder="Telephone (Home)" tabindex="4" type="text">\
    <p class="form-label"><label for="'+ parent_id + '_tel_mob">Telephone (Mobile)</label></p>\
    <input id="'+ parent_id + '_tel_mobile"  class="' + page + '" name="' + parent_id + '_tel_mobile" placeholder="Telephone (Mobile)" tabindex="4" type="text">\
    <p class="form-label"><label for="'+ parent_id + '_tel_work">Telephone (Work) </label></p>\
    <input id="'+ parent_id + '_tel_work"  class="' + page + '" name="' + parent_id + '_tel_work" placeholder="Telephone (Work)" tabindex="4" type="text">\
    <p class="form-label"><label for="'+ parent_id + '_email">Email </label></p>\
    <input id="'+ parent_id + '_email"  class="' + page + '" name="' + parent_id + '_email" placeholder="Email" tabindex="4" type="text">';
    $("#" + parent_id).html(div_html)
}

function add_student_page() {
    var page = "students";
    student_id += 1;
    var title = "Student-" + student_id + " Details";
    var delete_btn_html = "";
    var student_str = "student_" + student_id;
    if (student_id > 1)
        delete_btn_html = '<input type="button" name="delete" class="delstudent action-button" value="Delete Student"/>'
    var div_html = '\
    <div id='+ student_str + '">\
        <h3 class="fs-title">'+ title + '</h3>\
        <div  class="row">\
            <div class=col-md-6>\
                <p class="form-label"><label for="'+ student_str + '_surname_eng">Surname (Eng) </label></p>\
                <input id="'+ student_str + '_surname_eng" class="' + page + '" name="' + student_str + '_surname_eng" placeholder="Surname (Eng)" tabindex="1" type="text" required>\
            </div>\
            <div class=col-md-6>\
                <p class="form-label"><label for="'+ student_str + '_givenname_eng">Surname (Eng) </label></p>\
                <input id="'+ student_str + '_givenname_eng" class="' + page + '" name="' + student_str + '_givenname_eng" placeholder="Surname (Eng)" tabindex="1" type="text" required>\
            </div>\
        </div>\
        <div  class="row">\
            <div class=col-md-6>\
                <p class="form-label"><label for="'+ student_str + '_surname_tamil">Surname (Tamil) </label></p>\
                <input id="'+ student_str + '_surname_tamil" class="' + page + ' tamil" name="' + student_str + '_surname_tamil" placeholder="Surname (Tamil)" tabindex="1" type="text" >\
            </div>\
            <div class=col-md-6>\
                <p class="form-label"><label for="'+ student_str + '_givenname_tamil">Gieven Name (Tamil) </label></p>\
                <input id="'+ student_str + '_givenname_tamil" class="' + page + ' tamil" name="' + student_str + '_givenname_tamil" placeholder="Given Name (Tamil)" tabindex="1" type="text" >\
            </div>\
        </div>\
        <div  class="row">\
            <div class=col-md-6>\
                <p class="form-label"><label for="'+ student_str + '_dob">Date of Birth </label></p>\
                <input id="'+ student_str + '_dob" class="' + page + '" name="' + student_str + '_dob" placeholder="Date of Birth" tabindex="1" type="text" required>\
            </div>\
            <div class=col-md-6>\
                <p class="form-label"><label for="'+ student_str + '_sex">Gender </label></p>\
                  <span class="select-wrapper">\
                    <select id="'+ student_str + '_sex" class="' + page + '" name="' + student_str + '_sex" tabindex="0">\
                        <option value="" selected></option>\
                        <option value="Male">Male</option>\
                        <option value="Famale">Famale</option>\
                    </select>\
                </span>\
            </div>\
        </div>\
        <div  class="row">\
            <div class=col-md-6>\
                <p class="form-label"><label for="'+ student_str + '_res_status">Residential Status </label></p>\
                <input id="'+ student_str + '_res_status" class="' + page + '" name="' + student_str + '_res_status" placeholder="Residential Status" tabindex="1" type="text" required>\
            </div>\
            <div class=col-md-6>\
                <p class="form-label"><label for="'+ student_str + '_prev_studied">Did she / he attend Brisbane Tamil School last year? </label></p>\
                <span class="select-wrapper">\
                    <select id="'+ student_str + '_prev_studied" class="' + page + '" name="' + student_str + '_prev_studied" tabindex="0">\
                        <option value="" selected></option>\
                        <option value="Yes">Yes</option>\
                        <option value="No">No</option>\
                    </select>\
                </span>\
                </div>\
        </div>\
        <div class="row" style="padding: 0px 15px 0px 15px">\
            <p class="form-label"><label for="'+ student_str + '_school">Mainstream School </label></p>\
            <div class=row>\
                <div class=col-md-6>\
                    <input id="'+ student_str + '_school" class="' + page + '" name="' + student_str + '_school" placeholder="Mainstream School" tabindex="1" type="text" required>\
                </div>\
                <div class=col-md-6>\
                    <input id="'+ student_str + '_class" class="' + page + '" name="' + student_str + '_class" placeholder="Class at Mainstream School" tabindex="1" type="text" required>\
                </div>\
            </div>\
        <div class="row" style="margin-top: 5px;">\
                <div class=col-md-6>\
                    <input id="'+ student_str + '_school_street" class="' + page + '" name="' + student_str + '_school_street" placeholder="No, Street" tabindex="1" type="text" required>\
                </div>\
                <div class="col-md-4">\
                    <input id="'+ student_str + '_school_suburb" class="' + page + '" name="' + student_str + '_school_suburb" placeholder="Suburb" tabindex="1" type="text" required>\
                </div>\
                <div class="col-md-2">\
                    <input id="'+ student_str + '_school_postcode" class="' + page + '" name="' + student_str + '_school_postcode" placeholder="Postcode" tabindex="1" type="text" required>\
                </div>\
            </div>\
        </div>\
        <div class="row" style="padding: 0 15px 0 15px">\
            <p class="form-label"><label for="'+ student_str + '_doctor">Details of Family Doctor </label></p>\
            <div class="row">\
                <div class=col-md-6>\
                    <input id="'+ student_str + '_doctor_name" class="' + page + '" name="' + student_str + '_doctor_name" placeholder="Doctor Name" tabindex="1" type="text" required>\
                </div>\
                <div class="col-md-6">\
                    <input id="'+ student_str + '_doctor_tel" class="' + page + '" name="' + student_str + '_doctor_tel" placeholder="Doctor Tel" tabindex="1" type="text" required>\
                </div>\
            </div>\
            <div class="row" style="margin-top: 5px;">\
                <div class=col-md-6>\
                    <input id="'+ student_str + '_doctor_street" class="' + page + '" name="' + student_str + '_doctor_street" placeholder="No, Street" tabindex="1" type="text" required>\
                </div>\
                <div class="col-md-4">\
                    <input id="'+ student_str + '_doctor_suburb" class="' + page + '" name="' + student_str + '_doctor_suburb" placeholder="Suburb" tabindex="1" type="text" required>\
                </div>\
                <div class="col-md-2">\
                    <input id="'+ student_str + '_doctor_postcode" class="' + page + '" name="' + student_str + '_doctor_postcode" placeholder="Postcode" tabindex="1" type="text" required>\
                </div>\
            </div>\
        </div>\
        <div class="row">\
            <div class=col-md-12>\
                <p class="form-label"><label for="'+ student_str + '_med_cond">Are there any medical conditions that the school needs to know of?\
                </label></p>\
                <input id="'+ student_str + '_med_cond" class="' + page + '" name="' + student_str + '_med_cond" placeholder="Any medical conditions" tabindex="1" type="text" required>\
            </div>\
        </div>\
        <div class="row">\
            <div class=col-md-12>\
                <p class="form-label"><label for="'+ student_str + '_sports_cond">Are there any restrictions for normal or contact sports (state them)\
                </label></p>\
                <input id="'+ student_str + '_sports_cond" class="' + page + '" name="' + student_str + '_sports_cond" placeholder="Any restrictions for normal or contact sports" tabindex="1" type="text" required>\
            </div>\
        </div>\
    </div>'
        + delete_btn_html + '\
    <input type="button" name="add" class="addstudent action-button" value="Add Student"/>\
    <input type="button" name="previous" class="previous action-button" value="Previous"/>\
    <input type="button" name="next" class="next action-button" value="Next"/>\
    </div>';
    $("#students").append(div_html);
    //adding validations
    add_click_events();
    tamil_ids.push(student_str + "_surname_tamil");
    tamil_ids.push(student_str + "_givenname_tamil");
    google.setOnLoadCallback(onLoad);
}


const formToJSON = elements => [].reduce.call(elements, (data, element) => {
    data[element.name] = element.value;
    return data;
}, {});

$(document).ready(function () {
    var page = "parents";
    add_parent_fields("parent1", "FATHER / GURDIAN1", page);
    add_parent_fields("parent2", "MOTHER / GURDIAN2", page);
    add_student_page();
    validator = add_validator();
    $('#msform').on('submit', function (event) {
        var form_data = formToJSON($('#msform').serializeArray());
        var data_to_send = { "no_of_students": student_id, "year": year, "form_data": form_data };
        $.ajax({
            type: 'POST',
            url: 'submit_registration/',
            dataType: 'json',
            data: JSON.stringify(data_to_send),
            contentType: "application/json",
            success: function (data) {
                show_popup_alert("Success", "You have successfully submitted your enrolment form. You will receive a confirmation shortly.", 'info');
            }
        });

        //    return false;
    });

});

function add_validator() {
    return $("form[name='registration']").validate({
        // Specify validation rules
        rules: {
            parent1_surname: "required",
            parent1_givenname: "required",
            parent1_res_street: "required",
            parent1_res_suburb: "required",
            parent1_res_postcode: "required",
            parent1_email: {
                required: true,
                email: true
            },
            parent1_tel_mob: {
                required: true,
                digits: true,
                minlength: 10,
                maxlength: 10

            },

            parent2_email: {
                email: true
            },
            parent2_tel_mob: {
                digits: true,
                minlength: 10,
                maxlength: 10
            },
        },
        // Specify validation error messages
        messages: {
            parent1_title: "*Required",
            parent1_surname: "*Required",
            parent1_givenname: "*Required",
            parent1_email: {
                required: "*Required",
                email: "Email is not valid"
            },
            parent1_tel_mob: {
                required: "*Required",
                digits: "Only numbers allowed",
                minlength: "Requires 10 digits",
                maxlength: "Requires 10 digits"
            },

        },
        submitHandler: function (form) {
            // form.submit();
        }
    });

}
