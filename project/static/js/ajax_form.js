$(document).ready(function() {
    
        $('.captcha-refresh').click(function(){
            var $form = $(this).parents('form');
            var url = location.protocol + "//" + window.location.hostname + ":"
                      + location.port + "/captcha/refresh/";
            $.getJSON(url, {}, function(json) {
                $form.find('input[name="captcha_0"]').val(json.key);
                $form.find('img.captcha').attr('src', json.image_url);
            });

            return false;
        });

    
    
            function block_form() {
                $("#loading").show();
                $('textarea').attr('disabled', 'disabled');
                $('input').attr('disabled', 'disabled');
            }

            function unblock_form() {
                $('#loading').hide();
                $('textarea').removeAttr('disabled');
                $('input').removeAttr('disabled');
                $('.errorlist').remove();
            }

            // prepare Options Object for plugin
            var options = {
                beforeSubmit: function(form, options) {
                    // return false to cancel submit
                    block_form();
                },
                success: function(data) {
                    //alert(data);
                    path = data.redirect_url;
                    if (path){
                        //window.location.href +
                        window.location.href = path;
                        }
                    else{
                        location.reload();
                        }
//                    unblock_form();
//                    $("#form_ajax").show();
//                    setTimeout(function() {
//                        $("#form_ajax").hide();
//                    }, 5000);
                },
                error:  function(resp) {
                    unblock_form();
                    $("#form_ajax_error").show();
                    // render errors in form fields
                    var errors = JSON.parse(resp.responseText);
                    //alert(errors);
                    for (error in errors) {
                        //alert(error);
                        if (error=='captcha'){
                            var id = '#id_captcha_1';
                        }else{
                            var id = '#id_' + error;
                        }
                        $(id).parent('p').prepend(errors[error]);
                    }
                    if (errors == None){
                        Raven.captureException(resp);
                        }
                    setTimeout(function() {
                        $("#form_ajax_error").hide();
                    }, 5000);
                }
            };
            $('.ajaxform').ajaxForm(options);
    });
