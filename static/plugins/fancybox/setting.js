// jquery ready start
$(document).ready(function() {
	// jQuery code
	
// fancybox
	$('.fancybox').fancybox();

	$(".fancybox-form").fancybox({
		maxWidth	: 400,
		'overlayShow'		: true,
		'autoScale'			: false,
		openEffect	: 'elastic',
    	closeEffect	: 'elastic',
		helpers : {
			title	: { type : 'inside' },
			overlay : {	css : {'background' : 'rgba(0,0,0,.5)'}	}
		}
	});	
  
  
}); 
// jquery end
  