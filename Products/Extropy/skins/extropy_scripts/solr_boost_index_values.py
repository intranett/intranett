## Script (Python) "solr_boost_index_values"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=data
##title=Calculate field and document boost values for Solr

# this script is meant to be customized according to site-specific
# search requirements, e.g. boosting certain content types like "news items",
# ranking older content lower, consider special important content items,
# content rating etc.
#
# the indexing data that will be sent to Solr is passed in as the `data`
# parameter, the indexable object is available via the `context` binding.
# the return value should be a dictionary consisting of field names and
# their respecitive boost values.  use an empty string as the key to set
# a boost value for the entire document/content item.

result = {}
doc_boost = 1

# Penalize irc logs
if 'irc log' in data.get('Title', '').lower():
    return {'': 0.3}

# Boost items higher up in the hierarchy, the root gets 2, level 10 or
# deeper all get 1. For examaple /site/folder/page gets 1.6
depth = data.get('physicalDepth', 10)
depth_boost = max(2.0 - (depth / 10.0), 1)
doc_boost *= depth_boost

result[''] = doc_boost
return result
