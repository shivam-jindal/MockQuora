/*
Template: Knowledge Q&A Dashboard Template
Author: ScriptsBundle
Version: 1.0
Designed and Development by: ScriptsBundle
*/


(function($) {
        "use strict";
$('a[href*="#"]:not([href="#"])').on('click', function() {
    if (location.pathname.replace(/^\//,'') === this.pathname.replace(/^\//,'') && location.hostname === this.hostname) {
      var target = $(this.hash);
      target = target.length ? target : $('[name=' + this.hash.slice(1) +']');
      if (target.length) {
        $('html, body').animate({
          scrollTop: target.offset().top
        }, 1000);
        return false;
      }
    }
});

})(jQuery);
