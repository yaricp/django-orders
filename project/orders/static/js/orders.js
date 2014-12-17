$(document).ready(function() {
    $('#popup-order-form').css('display','none');
    $('#popup-edit-typework-form').css('display','none');
});

function load_form(url){
        $('#popup-order-form').load(url);
        $('#popup-order-form').dialog({
            modal:true,
            autoOpen: false,
        });
        $('#popup-order-form').dialog('open');
    };

function load_edit_typework_form(pk){
        if (pk==0){
                url='/orders/create_type_work'
            }
        else{
                url='/orders/type_work/'+pk+'/edit'
            }
        $('#popup-edit-typework-form').load(url);
        $('#popup-edit-typework-form').dialog({
            modal:true,
            autoOpen: false,
        });
        $('#popup-edit-typework-form').dialog('open');
    };
