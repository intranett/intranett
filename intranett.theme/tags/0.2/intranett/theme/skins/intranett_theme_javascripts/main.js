(function($) { 
    $(function() {
        jQuery.fn.jBreadCrumb.defaults.endElementsToLeaveOpen = 2;
        jQuery.fn.jBreadCrumb.defaults.beginingElementsToLeaveOpen = 2;
        jQuery.fn.jBreadCrumb.defaults.maxFinalElementLength = 300;        
        jQuery.fn.jBreadCrumb.defaults.previewWidth = 15;           
        $("#portal-breadcrumbs").jBreadCrumb(); 
        
        // Equal height for frontpage promo blocks 
        var heightEqualizer = function(elems, base_height) {
            if(elems.eq(0).hasClass("equalized")) {
                return false;
            }
            if(base_height == 0) {
                base_height = Math.max.apply(null, elems.map(function() { return $(this).height() }).get());           
                elems.height(base_height);
                elems.each(function() {
                    if($(this).find("img").length == 0) {
                        $(this).addClass("equalized");                    
                    }                
                });
            }
            else {
                // if we pass base_height we make inner elements fill the 
                // whole height
                $(elems).each( function() {
                    var outerStuff = $(this).outerHeight(true) - $(this).height();
                    var elemHeight = base_height - outerStuff; 
                    $(this).height(elemHeight);           
                })           
            }
            return base_height;
        }
        
        $(".photoAlbumEntryRow").each(function(){
            heightEqualizer($(this).find(".photoAlbumEntry"), 0);
        })                
        
        heightEqualizer($("dl.portalMessage dt, dl.portalMessage dd"), 0);
        
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
        });
        // $("table.listing tr").hover(
        //     function() {
        //         $(this).addClass("visualHighlight");                
        //     },
        //     function() {
        //         $(this).removeClass("visualHighlight");                
        //     }
        // );            
    }); 
})(jQuery);