$(document).ready(function(){

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

        $("#seat-number").html(selectedSeat.attr("seat-number"))

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
