var livesearch = (function () {

    var search_delay, hide_delay, searchhandlers, LSHighlight;

    // Delay in milliseconds until the search starts after the last key was
    // pressed. This keeps the number of requests to the server low.
    search_delay = 400;
    // Delay in milliseconds until the results window closes after the
    // searchbox looses focus.
    hide_delay = 400;

    // stores information for each searchbox on the page
    searchhandlers = {};

    // constants for better compression
    LSHighlight = "LSHighlight";

    function searchfactory($form, $inputnode) {
        // returns the search functions in a dictionary.
        // we need a factory to get a local scope for the event, this is
        // necessary, because IE doesn't have a way to get the target of
        // an event in a way we need it.
        var $lastsearch, $request, $cache, $querytarget, $$result, $shadow, $path;

        $lastsearch = null;
        $request = null;
        $cache = {};
        $querytarget = "livesearch_reply";
        $querytarget = $form.attr('action').replace(/search$/g, "") + $querytarget;
        $$result = $form.find('div.LSResult');
        $shadow = $form.find('div.LSShadow');
        $path = $form.find('input[name=path]');

        function hide() {
            // hides the result window
            // jQuery($$result).find(".livesearchContainer").animate({
            //     opacity:'toggle',
            //     height:'toggle'
            // }, 'fast', 'linear', function () {
            //     jQuery($$result).find(".toolTipArrow").fadeOut('slow');                
            // });
            jQuery($$result).find(".livesearchContainer, .LSIEFix").slideUp('fast', function () {
                jQuery($$result).find(".toolTipArrow").fadeOut(100, function () {
                    $$result.hide();
                    jQuery($$result).find(".toolTipArrow").show();
                });
            });
            $lastsearch = null;
        }

        function hide_delayed() {
            // hides the result window after a short delay
            window.setTimeout(
                'livesearch.hide("' + $form.attr('id') + '")',
                hide_delay);
        }

        function show($data) {
            // shows the result
            if ((jQuery($$result).find(".livesearchContainer").length === 0) || jQuery($$result).find(".livesearchContainer").is(":hidden")) {
                $shadow.html($data);
                jQuery($$result).find(".livesearchContainer").hide();
                $$result.show();
                jQuery(".livesearchContainer").animate({
                    opacity: 'toggle',
                    height: 'toggle'
                }, 'fast', 'swing');
            } else {
                $$result.show();
                $shadow.html($data);
            }
        }

        function search() {
            // does the actual search
            if ($lastsearch === $inputnode.value) {
                // do nothing if the input didn't change
                return;
            }
            $lastsearch = $inputnode.value;

            if ($request && $request.readyState < 4) {
                // abort any pending request
                $request.abort();
            }

            // Do nothing as long as we have less then two characters - 
            // the search results makes no sense, and it's harder on the server.
            if ($inputnode.value.length < 2) {
                hide();
                return;
            }

            var $$query = { q: $inputnode.value };
            if ($path.length && $path[0].checked) {
                $$query.path = $path.val();
            }
            // turn into a string for use as a cache key
            $$query = jQuery.param($$query);

            // check cache
            if ($cache[$$query]) {
                show($cache[$$query]);
                return;
            }

            // the search request (retrieve as text, not a document)
            $request = jQuery.get($querytarget, $$query, function ($data) {
                // show results if there are any and cache them
                show($data);
                $cache[$$query] = $data;
            }, 'text');
        }

        function search_delayed() {
            // search after a small delay, used by onfocus
            window.setTimeout(
                'livesearch.search("' + $form.attr('id') + '")', 
                search_delay);
        }

        return {
            hide: hide,
            hide_delayed: hide_delayed,
            search: search,
            search_delayed: search_delayed
        };
    }

    function keyhandlerfactory($form) {
        // returns the key event handler functions in a dictionary.
        // we need a factory to get a local scope for the event, this is
        // necessary, because IE doesn't have a way to get the target of
        // an event in a way we need it.
        var $timeout, $$result, $shadow, $cur, $prev, $next;

        $timeout = null;
        $$result = $form.find('div.LSResult');
        $shadow = $form.find('div.LSShadow');

        function keyUp() {
            // select the previous element
            $cur = $shadow.find('li.LSHighlight').removeClass(LSHighlight);
            $prev = $cur.prev('li');
            if (!$prev.length) {
                $prev = $shadow.find('li:last');
            }
            $prev.addClass(LSHighlight);
            return false;
        }

        function keyDown() {
            // select the next element
            $cur = $shadow.find('li.LSHighlight').removeClass(LSHighlight);
            $next = $cur.next('li');
            if (!$next.length) {
                $next = $shadow.find('li:first');
            }
            $next.addClass(LSHighlight);
            return false;
        }

        function keyEscape() {
            // hide results window
            $shadow.find('li.LSHighlight').removeClass(LSHighlight);
            $$result.hide();
        }

        function handler($event) {
            // dispatch to specific functions and handle the search timer
            window.clearTimeout($timeout);
            switch ($event.keyCode) {
            case 38:
                return keyUp();
            case 40:
                return keyDown();
            case 27:
                return keyEscape();
            case 37:
                break; // keyLeft
            case 39:
                break; // keyRight
            default:
                $timeout = window.setTimeout('livesearch.search("' + $form.attr('id') + '")', search_delay);
            }
        }

        function submit() {
            // check whether a search result was selected with the keyboard
            // and open it
            var $target = $shadow.find('li.LSHighlight a').attr('href');
            if (!$target) {
                return;
            }
            window.location = $target;
            return false;
        }

        return {
            handler: handler,
            submit: submit
        };
    }

    function setup(i) {
        var $id, $form, $keyhandler;

        // add an id which is used by other functions to find the correct node
        $id = 'livesearch' + i;
        $form = jQuery(this).parents('form:first');
        $keyhandler = keyhandlerfactory($form);
        searchhandlers[$id] = searchfactory($form, this);

        $form.attr('id', $id).css('white-space', 'nowrap').submit($keyhandler.submit);
        jQuery(this).attr('autocomplete', 'off')
               .keydown($keyhandler.handler)
               .focus(searchhandlers[$id].search_delayed)
               .blur(searchhandlers[$id].hide_delayed);
    }

    jQuery(function () {
        // find all search fields and set them up
        jQuery("#searchGadget,input.portlet-search-gadget").each(setup);
    });

    return {
        search: function (id) {
            searchhandlers[id].search();
        },
        hide: function (id) {
            searchhandlers[id].hide();
        }
    };
}());
