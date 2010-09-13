(function($) { 
    $(function() {
        jQuery.fn.jBreadCrumb.defaults.endElementsToLeaveOpen = 2;
        jQuery.fn.jBreadCrumb.defaults.beginingElementsToLeaveOpen = 2;
        jQuery.fn.jBreadCrumb.defaults.maxFinalElementLength = 300;        
        jQuery.fn.jBreadCrumb.defaults.previewWidth = 15;           
        $("#portal-breadcrumbs").jBreadCrumb(); 
        
        $("#open-edit-bar").click(function() {
            // $("#contentviews-wrapper").stop(); 
            $("#contentviews-wrapper, #contentviews-wrapper + .contentActions").animate({
                height: ['toggle', 'swing'],                
                opacity: 'toggle'
            }, 500, 'linear', function() {
                $("#open-edit-bar").fadeOut(200);
            });                      
            // $(this).toggleClass("expandedButton");
            return false;
        })
        $("#close-edit-bar").click(function() {
            // $("#contentviews-wrapper").stop(); 
            $("#contentviews-wrapper, #contentviews-wrapper + .contentActions").animate({
                height: ['toggle', 'swing'],                
                opacity: 'toggle'
            }, 500, 'linear', function() {
                $("#open-edit-bar").fadeIn(300);
            });                     
            // $(this).toggleClass("expandedButton");
            return false;
        })        
    }); 
})(jQuery);