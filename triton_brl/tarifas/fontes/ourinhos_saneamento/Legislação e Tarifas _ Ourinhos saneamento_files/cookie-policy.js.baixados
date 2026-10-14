$(function(){
    if(localStorage.getItem('cookieSeen') != 'shown'){
        $("#cookie-banner").delay(1000).fadeIn();
    }

    $('#cookie-banner .close').on('click', function(e) {
        localStorage.setItem('cookieSeen','shown');
        $('#cookie-banner').fadeOut(); 
    });
});