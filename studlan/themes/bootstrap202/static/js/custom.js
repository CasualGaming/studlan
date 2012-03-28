$('.alert-message').alert();

$.ajaxSetup ({  
    cache: false  
}); 

$("a.close").live("click", function() {
    $(this).load('{% url root %}/misc/remove_alert.html');
});
$(function () {
    $("a[rel=popover]")
        .popover({
            offset: 10
        })
        .click(function(e) {
            e.preventDefault()
        })
});
$(document).ready(function(){
    // Target your .container, .wrapper, .post, etc.
    $(".content").fitVids();
});
