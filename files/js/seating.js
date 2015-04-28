$(document).ready(function(){
	$("#seat-info-well").hide()
	$('a').mouseover( function() {
		//alert($(this).attr('title'));
		
		if($(this).attr('title')  !== undefined){
			$("#seat-info-well").show()
			document.getElementById('seat-info').innerHTML = $(this).attr('title');
		}
	} );
	$('svg').mouseleave( function() {
		$("#seat-info-well").hide()

	}
		);
} );
