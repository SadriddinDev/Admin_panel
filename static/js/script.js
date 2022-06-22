// some scripts

// jquery ready start
$(document).ready(function() {
	// jQuery code
	
	$('.carousel').carousel({
  		interval: 2000,
  		pause: false
	});

	// footer height
	var footer_h = $('#footer').height();
	$('.footer-space').css('margin-bottom', footer_h+'px')
	
	////scroll top
	var scroll_btn = $("a[href='#top']");
	scroll_btn.hide();
		$(window).scroll(function(){
			if ($(this).scrollTop() > 500) {
				scroll_btn.fadeIn();
			} else {
				scroll_btn.fadeOut();
			}
	    });
	    scroll_btn.click(function () {
			$("html, body").animate({ scrollTop: 0 }, "slow");               
			return false;
	});
}); 
// jquery end