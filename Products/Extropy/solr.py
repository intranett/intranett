from copy import copy

from collective.solr.manager import BaseSolrConnectionConfig


solr_config = BaseSolrConnectionConfig()
solr_config.active = True
solr_config.host = '127.0.0.1'
solr_config.port = 10093
solr_config.base = '/solr'
solr_config.async = True
solr_config.index_timeout = 0.0
solr_config.search_timeout = 0.0
solr_config.max_results = 500
solr_config.required = ('SearchableText', 'facet', 'use_solr', )
solr_config.facets = ('portal_type', )
solr_config.filter_queries = (
    'allowedRolesAndUsers',
    'effective',
    'expires',
    'is_default_page',
    'object_provides',
    'path',
    'parentPaths',
    'physicalDepth',
    'portal_type',
    'review_state',
    'Type',
)

solr_test_config = copy(solr_config)

from collective.solr import mangler
from collective.solr.search import quote
from DateTime import DateTime

def lowres_convert(value):
    """ convert values, which need a special format, i.e. dates """
    if isinstance(value, DateTime):
        v = value.toZone('UTC')
        # Lower date resolution to multiples of 15 minutes
        minute = v.minute() / 15 * 15
        value = '%04d-%02d-%02dT%02d:%02d:000Z' % (v.year(),
            v.month(), v.day(), v.hour(), minute)
    elif isinstance(value, basestring):
        value = quote(value)
    return value

mangler.convert = lowres_convert
