"""
A tour has this shape:

    {'tourId': u'example_tour',
     'title': _(u"Example tour"),
     'steps': <steps>}

<steps> has this shape:

    ({'url': u'/',
      'xpath': u'',
      'xcontent': u'',
      'title': _(u"Some title"),
      'text': _(u"Some text"),
      'steps': ({'description': _(u"Some description"),
                 'idStep': u'',
                 'selector': u'',
                 'text': u''},
                ...
               )       
     },
     ...
    )
                      
                      
The set of current tour's steps:

 - the description for the user (use [] to <span class="ajHighlight">highlight</span> parts), 
 - the step id, [see collective.amberjack.core.javascript.ajStandardSteps.ajStandardSteps]
 - an optional selector
 - an optional text used by the step

"""
