$(document).ready(function() {
    $('#popup-form').css('display','none');
    
    
});

function load_form(url){
        // url='../edit_profile'
        $('#popup-form').load(url);
        $('#popup-form').dialog({
            modal:true,
            autoOpen: false,
        });
        $('#popup-form').dialog('open');
    };
