from copy import copy

from collective.solr.manager import BaseSolrConnectionConfig


solr_config = BaseSolrConnectionConfig()
solr_config.active = True
solr_config.host = '127.0.0.1'
solr_config.port = 10093
solr_config.base = '/solr'
solr_config.async = True
solr_config.auto_commit = False
solr_config.commit_within = 60000 # 60 seconds
solr_config.effective_steps = 900 # 15 minutes
solr_config.index_timeout = 30.0
solr_config.search_pattern = \
    '(Title:{value}^5 OR Description:{value}^2 OR SearchableText:{value} ' \
    'OR SearchableText:{base_value})'
solr_config.search_timeout = 30.0
solr_config.slow_query_threshold = 1000 # 1 second
solr_config.max_results = 100
solr_config.required = ('SearchableText', 'facet', )
solr_config.facets = ('portal_type', )
solr_config.filter_queries = (
    'allowedRolesAndUsers effective expires',
    'portal_type review_state',
    'allowedRolesAndUsers',
    'effective',
    'expires',
    'is_default_page',
    'object_provides',
    'parentPaths',
    'path',
    'physicalDepth',
    'portal_type',
    'review_state',
    'Type',
)

solr_test_config = copy(solr_config)
