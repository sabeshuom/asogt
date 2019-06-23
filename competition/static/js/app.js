$(document).ready(function() {
    check_authentication(true);
  $('#popup-login').on('hidden.bs.modal', function (e) {
        check_authentication(true);
  });
    $('.dropdown-menu a').click(function(){
        $(this).parent().parent().parent().find(".selected").text($(this).text());
    });
});

