$(document).ready(function(){


    ['preserveAspectRatio', 'viewBox'].forEach(function(k) {
      // jQuery converts the attribute name to lowercase before
      // looking for the hook.
      $.attrHooks[k.toLowerCase()] = {
        set: function(el, value) {
          if (value) {
            el.setAttribute(k, value);
          } else {
            el.removeAttribute(k, value);
          }
          return true;
        },
        get: function(el) {
          return el.getAttribute(k);
        },
      };
    });

    var main_svg = $("#seating-svg-wrapper > svg");

    if (main_svg.attr("viewBox") === undefined){
        main_svg.attr({
            viewBox: [0,0, main_svg.attr('width').replace('px', ''),main_svg.attr('height').replace('px', '')].join(' ')
        });
    }

    main_svg.attr({
        preserveAspectRatio: "xMidYMid meet"
    });

    main_svg.removeAttr("width");
    main_svg.removeAttr("height");

    var selectedSeat;
    var selectedSeatClass;

    $('a > rect').click( function(e) {
        e.preventDefault();

        if(selectedSeat){
            $(selectedSeat).attr("class", selectedSeatClass)
        }

        selectedSeat = $(this)

        selectedSeatClass = selectedSeat.attr('class')
        selectedSeat.attr("class", selectedSeatClass + " seating-node-info")

        $("#seat-number").html(selectedSeat.attr("seat-display"))

        if(selectedSeat.attr("status") === "occupied"){

            $("#seat-user").html(selectedSeat.attr("seat-user"))
            $("#occupied-by").removeClass("hide")
        }
        else{
            $("#occupied-by").addClass("hide")
        }

        // Set seat number in take and leave forms
        var seatNumber = selectedSeat.attr("seat-number")
        $(".seat-number-input").each(function() {
            this.value = seatNumber;
        });

        var takeForm = $('#take-form')
        if (takeForm) {
            if (selectedSeat.attr("status") === "free") {
                takeForm.removeClass("hide")
            } else{
                takeForm.addClass("hide")
            }
        }

        var leaveForm = $('#leave-form')
        if (leaveForm) {
            if (selectedSeat.attr("status") === "mine") {
                leaveForm.removeClass("hide")
            } else{
                leaveForm.addClass("hide")
            }
        }
    });

});
$(window).resize(function() {



});