function toggleArticle(article) {
    var curId = $(article).attr("id");
    // Expand
    if($("#"+curId).attr('style').indexOf("display: none;") >= 0) {
        $("#"+curId).slideToggle("slow", "linear", function() {
            $("#"+curId+"-icon").removeClass("icon-chevron-right").addClass("icon-chevron-down");
        });
    }
    // Shrink
    else {
        $("#"+curId).slideToggle("slow", "linear", function() {
            $("#"+curId+"-icon").removeClass("icon-chevron-down").addClass("icon-chevron-right");
        });
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
