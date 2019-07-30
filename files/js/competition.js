$(function () {
	// browser compatibility: get method for event 
    // addEventListener(FF, Webkit, Opera, IE9+) and attachEvent(IE5-8)
    var myEventMethod = window.addEventListener ? "addEventListener" : "attachEvent";
    var myEventListener = window[myEventMethod];

    // browser compatibility: attach event uses onmessage
    var myEventMessage = myEventMethod == "attachEvent" ? "onmessage" : "message";

    myEventListener(myEventMessage, function (e) {
        if (e.data === parseInt(e.data)) 
        	var height = e.data - 150;
            //document.getElementById('brackets-frame').height = height + "px";
	}, false);

    $('#brackets-button').click(function(e){
    	$('#brackets-container').toggleClass('hide');
    	if($(this).html() == 'Show brackets'){
    		$(this).html('Hide brackets')
    	}
    	else{
    		$(this).html('Show brackets')
    	}
    })
});

function AdjustIFrame(id) {
	window.onload = function() {
    	window.parent.postMessage(document.body.scrollHeight, "*")
	};
}