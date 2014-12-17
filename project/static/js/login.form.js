$(document).ready(function() {
    $('#popup-form').css('display','none');
    $('#login-div').click(function(){
        $('#popup-form').load('/accounts/login/');
        $('#popup-form').dialog({
            modal:true,
            autoOpen: false,
        });
        $('#popup-form').dialog('open');
    });

    $('#contacts').click(function(){
        $('#popup-form').load('/contacts/');
        $('#popup-form').dialog({
            modal:true,
            autoOpen: false,
        });
        $('#popup-form').dialog('open');
    });
    
    
});

function load_form(url){
    $('#popup-form').load(url);
    };

