$.ajaxSetup ({  
    cache: false  
}); 

window.setTimeout(function() {
  $(".flash").fadeTo(500, 0).slideUp(500, function(){
      $(this).remove();
  });
}, 5000);

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
