// jquery ready start
$(document).ready(function() {
	// jQuery code
	owl = $("#owl-blog");
	owl.owlCarousel({
		loop:true,
		items : 4,
		autoPlay : true,
		dots: true,
		autoplayTimeout : 5000,
		margin: 30,
		responsive : {
		    // breakpoint from 480 up
		    0 : {
		        items : 2
		    },
		    // breakpoint from 768 up
		    768 : {
		        items : 4
		    }
		}
	});
	

	// jQuery code
	owl_testimonal = $("#owl-testimonal");
	owl_testimonal.owlCarousel({
	loop:true,
	items : 1,
	autoPlay : true,
	dots: false,
	autoplayTimeout : 3000,
	margin: 15,
	nav : false,
	navText :	[" <i class='fa fa-chevron-left'></i> "," <i class='fa fa-chevron-right'></i> "]
	});

	// Custom Navigation Events
	$(".owl-next").click(function(){
		owl_testimonal.trigger('next.owl.carousel');
	});
	$(".owl-prev").click(function(){
		 owl_testimonal.trigger('prev.owl.carousel');
	});
	
}); 
// jquery end