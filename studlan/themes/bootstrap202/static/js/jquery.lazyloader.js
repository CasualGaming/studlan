/*
 * LazyLoader - A jquery extension to render images and html content as the user scrolls down the page.
 *
 * Copyright (c) 2011 Michael Collins
 *
 * Licensed under the MIT license:
 *   http://www.opensource.org/licenses/mit-license.php
 *
 * Project home:
 *  http://ivorycity.com/blog/
 *
 */

( function($) {

jQuery.fn.extend(
{
	lazyLoad: function()
	{
		var d = $(window).data('lazyloaders');
		if (!d)
		{
			d = [];
		}
		this.each( function() { d.push(this); } );
		$(window).data('lazyloaders', d );
	},
	
	showComment: function()
	{
		return this.each(function()
		{
			var child = this.firstChild;
			if (child.nodeType === 8) // 8 is a comment node
			{
				this.innerHTML = ''; // Fixes IE sometimes breaking with replaceWith() call
				$(this).replaceWith(child.nodeValue);
			}
		});
	}

});

$(document).ready( function()
{
	var scrolling = false;

	$(window).scroll( function()
	{
		//Prevent scroll stacking
		if (!scrolling)
		{
			scrolling = true;
			//don't unlock for 250ms
			setTimeout( function()
			{
				var d = $(window).data('lazyloaders');
				if (!d || !d.length)
				{
					return;
				}
	
				$( d ).each( function(i)
				{	
					if ( this && $.inviewport( this, {threshold:0} ) )
					{
						$(this).showComment();
					}
				});

				scrolling = false;			
			}, 250);
					
		}
	});

	$(window).trigger( 'scroll' );

});


/*
 * Viewport - jQuery selectors for finding elements in viewport
 *
 * Copyright (c) 2008-2009 Mika Tuupola
 *
 * Licensed under the MIT license:
 *   http://www.opensource.org/licenses/mit-license.php
 *
 * Project home:
 *  http://www.appelsiini.net/projects/viewport
 *
 */
    $.belowthefold = function(element, settings) {
        var fold = $(window).height() + $(window).scrollTop();
        return fold <= $(element).offset().top - settings.threshold;
    };

    $.abovethetop = function(element, settings) {
        var top = $(window).scrollTop();
        return top >= $(element).offset().top + $(element).height() - settings.threshold;
    };

    $.rightofscreen = function(element, settings) {
        var fold = $(window).width() + $(window).scrollLeft();
        return fold <= $(element).offset().left - settings.threshold;
    };

    $.leftofscreen = function(element, settings) {
        var left = $(window).scrollLeft();
        return left >= $(element).offset().left + $(element).width() - settings.threshold;
    };

    $.inviewport = function(element, settings) {
        return !$.rightofscreen(element, settings) && !$.leftofscreen(element, settings) && !$.belowthefold(element, settings) && !$.abovethetop(element, settings);
    };

    $.extend($.expr[':'], {
        "below-the-fold": function(a, i, m) {
            return $.belowthefold(a, {threshold : 0});
        },
        "above-the-top": function(a, i, m) {
            return $.abovethetop(a, {threshold : 0});
        },
        "left-of-screen": function(a, i, m) {
            return $.leftofscreen(a, {threshold : 0});
        },
        "right-of-screen": function(a, i, m) {
            return $.rightofscreen(a, {threshold : 0});
        },
        "in-viewport": function(a, i, m) {
            return $.inviewport(a, {threshold : 0});
        }
    });

})(jQuery);
