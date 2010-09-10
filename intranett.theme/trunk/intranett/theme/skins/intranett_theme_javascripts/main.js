(function($) { 
    $(function() {
        jQuery.fn.jBreadCrumb.defaults.endElementsToLeaveOpen = 2;
        jQuery.fn.jBreadCrumb.defaults.beginingElementsToLeaveOpen = 2;
        jQuery.fn.jBreadCrumb.defaults.maxFinalElementLength = 300;        
        jQuery.fn.jBreadCrumb.defaults.previewWidth = 15;           
        $("#portal-breadcrumbs").jBreadCrumb(); 
        
        $("#settings-toggle a").click(function() {
            // $("#contentviews-wrapper").stop(); 
            $("#contentviews-wrapper, #contentviews-wrapper + .contentActions").animate({
                height: ['toggle', 'swing'],                
                opacity: 'toggle'
            }, 500, 'linear', function() {
                // $("#settings-toggle a").fadeOut();
            });                      
            // $(this).toggleClass("expandedButton");
            return false;
        })
    }); 
})(jQuery);