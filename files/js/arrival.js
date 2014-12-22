/* AJAX SETUP FOR CSRF */
$.ajaxSetup({
    crossDomain: false, // obviates need for sameOrigin test
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type)) {
            xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'));
        }
    }
});
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
/* END AJAX SETUP */


function toggle(username, type, previousValue, label)
{
    $.ajax({
        method: 'POST',
        url: 'toggle/',
        data: {'username': username, 'type': type, 'prev': previousValue},
        success: function() {
            $(label).toggleClass("label-success label-danger");
            if(prev == "True")
            {
                $(label).attr('value', "False");
            }
            else if(prev == "False")
            {
                $(label).attr('value', "True");
            }
        },
        error: function(res) {
                alert(res['responseText']);
        },
        crossDomain: false
    });
}

$(document).ready(function()
{
     $('tr').each(function(i, row)
    {
        $(row).find('.paid').click(function()
        {
            username = $(row).find('.username').text();
            prev = $(this).attr('value');
            toggle(username, 0, prev, this);
        });
        $(row).find('.arrived').click(function()
        {
            username = $(row).find('.username').text();
            prev = $(this).attr('value');
            toggle(username, 1, prev, this);
        });
    });
        
});
