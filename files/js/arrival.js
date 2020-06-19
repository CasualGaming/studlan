
$(function() {
/* AJAX SETUP FOR CSRF */

//Getting the cookie from the html because the csrfcookie has security flaws when used 
//with client side js
function getToken(){
    var csrftoken = $('#token').val();
    return csrftoken;
}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    crossDomain: false, // obviates need for sameOrigin test
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type)) {
            xhr.setRequestHeader("X-CSRFToken", getToken());
        }
    }
});
/* END AJAX SETUP */

const TYPE_PAID = 0;
const TYPE_ARRIVED = 1;
const VALUE_YES = "True"
const VALUE_NO = "False"

function toggle(username, type, previousValue, label)
{
    let question_id;
    if (type == TYPE_PAID && previousValue == VALUE_NO) {
        question_id = "toggle-text-has-paid";
    } else if (type == TYPE_PAID && previousValue == VALUE_YES) {
        question_id = "toggle-text-has-not-paid";
    } else if (type == TYPE_ARRIVED && previousValue == VALUE_NO) {
        question_id = "toggle-text-has-arrived";
    } else if (type == TYPE_ARRIVED && previousValue == VALUE_YES) {
        question_id = "toggle-text-has-not-arrived";
    }
    let question = $("#" + question_id).text().replace("{user}", username);
    if (!confirm(question))
        return;

    $.ajax({
        method: 'POST',
        url: 'toggle/',
        data: {'username': username, 'type': type, 'prev': previousValue},
        success: function() {
            $(label).toggleClass("label-success label-danger");
            if(previousValue == VALUE_YES)
            {
                $(label).attr('value', VALUE_NO);
            }
            else if(previousValue == VALUE_NO)
            {
                $(label).attr('value', VALUE_YES);
            }
            updateTable();
        },
        error: function(res) {
            let message = res['responseText'];
            if (!message) {
                message = "No response.";
            }
            alert(message);
            console.log(message);
        },
        crossDomain: false
    });
}

$(document).ready(function()
{
     $('tr').each(function(i, row)
    {
        $(row).find('.paid.toggle').click(function()
        {
            var username = $(row).find('.username').text();
            var prev = $(this).attr('value');
            toggle(username, TYPE_PAID, prev, this);
        });
        $(row).find('.arrived.toggle').click(function()
        {
            var username = $(row).find('.username').text();
            var prev = $(this).attr('value');
            toggle(username, TYPE_ARRIVED, prev, this);
        });
    });     
});

let updateTable = function(){
    // Re-show all rows
    $(".filterable tr:hidden").show();

    // Filter paid
    let filterPaidRaw = $("#filter-paid-input").val().toLowerCase();
    if (filterPaidRaw === "yes" || filterPaidRaw === "no") {
        let selector = filterPaidRaw === "yes" ? "span.paid[value='True']" : "span.paid[value='False']";
        $(".filterable > tbody > tr:visible").each(function(){
            if ($("td > " + selector, this).length) {
                return;
            }
            $(this).hide();
        });
    }

    // Filter paid type
    let filterPaidType = $("#filter-paid-type-input").val().toLowerCase();
    const paidTypeManual = "__manual__";
    if (filterPaidType) {
        let isPaidTypeManual = filterPaidType === paidTypeManual;
        let selector = isPaidTypeManual ? "span.manual" : "span.ticket";
        $(".filterable > tbody > tr:visible").each(function(){
            if (isPaidTypeManual) {
                if (!$("td > " + selector, this).length) {
                    $(this).hide();
                }
            } else {
                let matches = $("td > " + selector, this);
                let found = false;
                matches.each(function(_, obj) {
                    if (obj.getAttribute("ticketType") === filterPaidType) {
                        found = true;
                    }
                });
                if (!found) {
                    $(this).hide();
                }
            }
        });
    }

    // Filter arrived
    let filterArrivedRaw = $("#filter-arrived-input").val().toLowerCase();
    if (filterArrivedRaw === "yes" || filterArrivedRaw === "no") {
        let selector = filterArrivedRaw === "yes" ? "span.arrived[value='True']" : "span.arrived[value='False']";
        $(".filterable > tbody > tr:visible").each(function(){
            if ($("td > " + selector, this).length) {
                return;
            }
            $(this).hide();
        });
    }

    // Filter text
    let filterText = $("#filter-text-input").val().toLowerCase();
    if (filterText) {
        $(".filterable > tbody > tr:visible").each(function(){
            if ($("td.username > a", this).text().toLowerCase().indexOf(filterText) != -1) {
                return;
            }
            if ($("td.name", this).text().toLowerCase().indexOf(filterText) != -1) {
                return;
            }
            if ($("td.email", this).text().toLowerCase().indexOf(filterText) != -1) {
                return;
            }
            $(this).hide();
        });
    }
}

$(document).ready(function(){
    // Focus filter field
    $("input:text:visible:first").focus();
    // Remove existing values and add triggers
    $("#filter-text-input").val("");
    $("#filter-text-input").keyup(updateTable);
    $("#filter-paid-input").val("");
    $("#filter-paid-input").change(updateTable);
    $("#filter-paid-type-input").val("");
    $("#filter-paid-type-input").change(updateTable);
    $("#filter-arrived-input").val("");
    $("#filter-arrived-input").change(updateTable);
});
});
