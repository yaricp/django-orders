$(document).ready(function() {
    $('.captcha-reload').on('click', function() {
        var img = $('img.captcha', $(this).parent());
        img.attr('src', img.attr('src').split('?', 1)+'?update=1&'+Math.random());
        return false;
    });
  })
