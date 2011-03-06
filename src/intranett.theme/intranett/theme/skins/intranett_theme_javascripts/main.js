/* The following line defines gliobal variables defined elsewhere. */
/*global jQuery:false, document: false, window: false*/

(function ($) {
    $.fn.heightEqualizer = function (base_height) {
        if ($(this).eq(0).hasClass('equalized')) {
            return false;
        }
        if (base_height === 0) {
            base_height = Math.max.apply(null, this.map(function () {
                return $(this).height();
            }).get());
            this.height(base_height);
            this.each(function () {
                if ($(this).find('img').length === 0) {
                    $(this).addClass('equalized');
                }
            });
        }
        else {
            // if we pass base_height we make inner elements fill the
            // whole height
            $(this).each(function () {
                var outerStuff, elemHeight;
                outerStuff = $(this).outerHeight(true) - $(this).height();
                elemHeight = base_height - outerStuff;
                $(this).height(elemHeight);
            });
        }
        return base_height;
    };
}(jQuery));

(function ($) {
    $(function () {
        jQuery.fn.jBreadCrumb.defaults.endElementsToLeaveOpen = 2;
        jQuery.fn.jBreadCrumb.defaults.beginingElementsToLeaveOpen = 2;
        jQuery.fn.jBreadCrumb.defaults.maxFinalElementLength = 300;
        jQuery.fn.jBreadCrumb.defaults.previewWidth = 15;
        $('#portal-breadcrumbs').jBreadCrumb();

        $('.photoAlbumEntryRow').each(function () {
            $(this).find('.photoAlbumEntry').heightEqualizer(0);
        });

        $('dl.portalMessage dt, dl.portalMessage dd').heightEqualizer(0);
        $('#frontpage-columns .fpBlock .visualPadding').heightEqualizer(0);

        $('#settings-toggle a').click(function (event) {
            event.stopPropagation();
            $('#contentviews-wrapper, #contentviews-wrapper + .contentActions').animate({
                height: ['toggle', 'swing'],
                opacity: 'toggle'
            }, 200, 'linear', function () {
                var isHidden = $('#open-edit-bar').is(':hidden');
                if (isHidden) {
                    $('#open-edit-bar').delay(0).fadeIn(200);
                    document.cookie = 'editbar_opened=0; expires=Fri, 27 Jul 2001 02:47:11 UTC; path=/';
                } else {
                    $('#open-edit-bar').delay(0).fadeOut(200); // delay in order to have both elements animated (contentMenus & contentActions) before we transform the button
                    document.cookie = 'editbar_opened=1; expires=0; path=/';
                }
            });
            return false;
        });
        $('#form-buttons-comment').addClass('allowMultiSubmit');
        $("a[class='form.button.DeleteComment']").live('click', function () {
            var trigger, form, data, form_url;
            trigger = this;
            form = $(this).parents('form');
            data = $(form).serialize();
            form_url = $(form).attr('action');
            $.ajax({
                type: 'POST',
                url: form_url,
                context: $(trigger).parents('.comment'),
                success: function (data) {
                    if ($('.discussion .comment').length === 1) {
                        $('.discussion').fadeOut('fast', function () {
                            $('.discussion').remove();
                        });
                    }
                    else {
                        $(this).fadeOut('fast', function () {
                            $(this).remove();
                        });
                    }
                },
                error: function (req, error) {
                    return true;
                }
            });
            return false;
        });
        $('#commenting form').submit(function () {
            var button, data, form_url;
            button = $('#commenting form #form-buttons-comment');
            $(button).attr('disabled', 'disabled');

            data = $('#commenting form').serialize() + '&' + $(button).attr('name') + '=' + $(button).attr('value');
            form_url = $(this).attr('action');
            $(this).get(0).reset();
            $.ajax({
                type: 'POST',
                url: form_url,
                data: data,
                success: function (data) {
                    var new_comment, jqobj;
                    jqobj = $(data);
                    if ($('.discussion').length > 0) {
                        new_comment = $(jqobj).find('.discussion .comment:last-child');
                        $(new_comment).hide();
                        $('.discussion').append(new_comment);
                    } else {
                        new_comment = $(jqobj).find('.discussion');
                        $(new_comment).hide();
                        $(new_comment).insertBefore('#commenting');
                    }
                    $(new_comment).fadeIn('slow');
                    $(button).removeAttr('disabled');
                },
                error: function (req, error) {
                    return true;
                }
            });
            return false;
        });
    });
}(jQuery));
