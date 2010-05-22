# query plan dumped at 'Sun Mar 28 14:41:09 2010'

queryplan = {
  '/intranet.psol/portal_catalog': {
  },
  '/intranet.psol/uid_catalog': {
    ('UID',):
      ['UID'],
  },
  '/intranet.psol/reference_catalog': {
    ('merge', 'sourceUID'):
      ['sourceUID'],
    ('merge', 'targetUID'):
      ['targetUID'],
  },
  '/intranet.psol/reference_catalog:valueindexes': frozenset([
    'relationship',
  ]),
  '/intranet.psol/extropy_tracking_tool': {
  },
  '/intranet.psol/extropy_tracking_tool:valueindexes': frozenset([
    'meta_type',
    'portal_type',
    'review_state',
  ]),
  '/intranet.psol/extropy_timetracker_tool': {
  },
  '/intranet.psol/extropy_timetracker_tool:valueindexes': frozenset([
    'getBudgetCategory',
    'review_state',
  ]),
}
