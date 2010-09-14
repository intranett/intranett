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
            }, 200, 'linear', function() {
                var working = 1;
                var isHidden = $("#open-edit-bar").is(":hidden");
                isHidden ? $("#open-edit-bar").delay(0).fadeIn(200) : $("#open-edit-bar").delay(0).fadeOut(200); // delay in order to have both elements animated (contentMenus & contentActions) before we transform the button
            });
            return false;
        })      
    }); 
})(jQuery);