function toggleArticle(article) {
    // Expand
    console.log(article);
    if($(article).attr('class').indexOf("hidden") >= 0) {
        $(article).slideDown("slow").removeClass("hidden");
    }
    // Shrink
    else {
        $(article).slideUp("slow");
        setTimeout('$(article).addClass("hidden");',500);
    }
}

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
            animation: true,
            trigger: "hover"
        })
        .click(function(e) {
            e.preventDefault()
        })
});
$(document).ready(function(){
    // Target your .container, .wrapper, .post, etc.
    $(".content").fitVids();
});
