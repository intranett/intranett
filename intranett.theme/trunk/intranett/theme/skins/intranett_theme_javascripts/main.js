(function($) { 
    $(function() {
        jQuery.fn.jBreadCrumb.defaults.endElementsToLeaveOpen = 2;
        jQuery.fn.jBreadCrumb.defaults.beginingElementsToLeaveOpen = 2;
        jQuery.fn.jBreadCrumb.defaults.maxFinalElementLength = 300;        
        jQuery.fn.jBreadCrumb.defaults.previewWidth = 15;           
        $("#portal-breadcrumbs").jBreadCrumb(); 
        
        $("#settings-toggle a").click(function(event) {
            event.stopPropagation(); 
            $("#contentviews-wrapper, #contentviews-wrapper + .contentActions").animate({
                height: ['toggle', 'swing'],                
                opacity: 'toggle'
            }, 200, 'linear', function() {
                var isHidden = $("#open-edit-bar").is(":hidden");
                if(isHidden){
                    $("#open-edit-bar").delay(0).fadeIn(200);
                    document.cookie = 'editbar_opened=0; expires=Fri, 27 Jul 2001 02:47:11 UTC; path=/';
                } else {
                    $("#open-edit-bar").delay(0).fadeOut(200); // delay in order to have both elements animated (contentMenus & contentActions) before we transform the button
                    document.cookie = 'editbar_opened=1; expires=0; path=/';                    
                }
            });
            return false;
        })
            
    }); 
})(jQuery);