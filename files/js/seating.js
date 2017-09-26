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

    var main_svg = $("#svg-wrapper > svg");
    var h = "60vh";
    if (main_svg.attr("viewBox") !== undefined || main_svg.attr("viewBox") !== false){
        main_svg.attr({
            viewBox: [0,0, main_svg.attr('width').replace('px', ''),main_svg.attr('height').replace('px', '')].join(' ')
        });
    }

    main_svg.attr({
        height: h,
        preserveAspectRatio: "xMidYMid meet"
    });

    main_svg.removeAttr("width");

    var selectedSeat;
    var selectedSeatClass;




    $('rect').click( function(e) {
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


        if(selectedSeat.attr("status") === "free"){

            var takeButton = $('#take-button')

            if(takeButton){
                takeButton.attr("href", selectedSeat.attr("seat-number") + "/take")
                takeButton.removeClass("hide")
            }
        }
        else{
            var takeButton = $('#take-button')

            if(takeButton){
                takeButton.addClass("hide")
            }
        }

        if(selectedSeat.attr("status") === "mine"){

            var leaveButton = $('#leave-button')

            if(leaveButton){
                leaveButton.attr("href", selectedSeat.attr("seat-number") + "/leave")
                leaveButton.removeClass("hide")
            }
        }
        else{
            var leaveButton = $('#leave-button')

            if(leaveButton){
                leaveButton.addClass("hide")
            }
        }

    });

});
$(window).resize(function() {



});