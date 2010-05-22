# query plan dumped at 'Sat May 22 23:16:22 2010'

queryplan = {
  '/intranet.psol/portal_catalog': {
    ('allowedRolesAndUsers', 'path', 'show_inactive', 'sort_on'):
      ['path', 'allowedRolesAndUsers'],
    ('allowedRolesAndUsers', 'path', 'show_inactive', 'sort_on', ('portal_type', "['Image', 'Document', 'Event', 'File', 'Invoice', 'ExtropyActivity']")):
      ['path', 'portal_type', 'allowedRolesAndUsers'],
    ('allowedRolesAndUsers', 'path', 'show_inactive', 'sort_on', ('portal_type', "['Image', 'Document', 'Event', 'Folder', 'File', 'Invoice']")):
      ['path', 'portal_type', 'allowedRolesAndUsers'],
    ('allowedRolesAndUsers', 'path', 'sort_on', 'sort_order', ('is_default_page', 'False'), ('is_folderish', 'True'), ('portal_type', "['ExtropyActivity', 'ExtropyPhase', 'ExtropyProject', 'Folder', 'Topic']"), ('review_state', "('Sent', 'active', 'prospective', 'open', 'assigned', 'entered', 'external', 'internal', 'internally_published', 'pending', 'planned', 'private', 'prospective', 'Draft', 'published', 'testing', 'unassigned')")):
      ['path', 'portal_type', 'is_folderish', 'review_state', 'is_default_page', 'allowedRolesAndUsers'],
    ('allowedRolesAndUsers', 'path', 'sort_on', 'sort_order', ('is_default_page', 'False'), ('portal_type', "['ATFile', 'ATImage', 'ExtropyActivity', 'ExtropyPhase', 'ExtropyProject', 'Folder', 'Large Plone Folder', 'Topic']"), ('review_state', "('Sent', 'active', 'prospective', 'open', 'assigned', 'entered', 'external', 'internal', 'internally_published', 'pending', 'planned', 'private', 'prospective', 'Draft', 'published', 'testing', 'unassigned')")):
      ['path', 'portal_type', 'review_state', 'is_default_page', 'allowedRolesAndUsers'],
    ('allowedRolesAndUsers', 'path', 'sort_on', ('portal_type', "'Invoice'")):
      ['path', 'portal_type', 'allowedRolesAndUsers'],
    ('allowedRolesAndUsers', 'path', 'sort_on', ('portal_type', "[u'Topic', u'Event', u'File', u'Folder', u'Image', u'Large Plone Folder', u'News Item', u'Document']")):
      ['path', 'portal_type', 'allowedRolesAndUsers'],
    ('allowedRolesAndUsers', 'path', ('Type', "'Invoice'")):
      ['Type', 'allowedRolesAndUsers', 'path'],
    ('allowedRolesAndUsers', 'sort_on', 'sort_order'):
      ['allowedRolesAndUsers'],
    ('path',):
      ['path'],
  },
  '/intranet.psol/portal_catalog:valueindexes': frozenset([
    'Subject',
    'Type',
    'in_reply_to',
    'is_default_page',
    'is_folderish',
    'meta_type',
    'portal_type',
    'review_state',
  ]),
  '/intranet.psol/uid_catalog': {
    ('UID',):
      ['UID'],
  },
  '/intranet.psol/reference_catalog': {
    ('merge', 'sourceUID'):
      ['sourceUID'],
    ('merge', 'sourceUID', ('relationship', "'invoice'")):
      ['sourceUID', 'relationship'],
    ('merge', 'sourceUID', ('relationship', "'relatesTo'")):
      ['sourceUID', 'relationship'],
    ('merge', 'targetUID'):
      ['targetUID'],
    ('sourceUID', ('relationship', "'relatesTo'")):
      ['sourceUID', 'relationship'],
  },
  '/intranet.psol/reference_catalog:valueindexes': frozenset([
    'relationship',
  ]),
  '/intranet.psol/extropy_tracking_tool': {
    ('allowedRolesAndUsers', 'getParticipants', ('portal_type', "'ExtropyProject'"), ('review_state', "'active'")):
      ['portal_type', 'getParticipants', 'review_state', 'allowedRolesAndUsers'],
    ('allowedRolesAndUsers', 'getResponsiblePerson', 'path', 'sort_on', ('portal_type', "['ExtropyTask', 'ExtropyActivity', 'ExtropyFeature']"), ('review_state', "['open', 'in-progress', 'active', 'unassigned', 'deferred', 'assigned', 'testing', 'taskscomplete']")):
      ['path', 'getResponsiblePerson', 'review_state', 'portal_type', 'allowedRolesAndUsers'],
    ('allowedRolesAndUsers', 'getResponsiblePerson', ('portal_type', "('ExtropyActivity', 'ExtropyFeature', 'ExtropyTask')"), ('review_state', "['open', 'in-progress', 'active', 'unassigned', 'deferred', 'assigned', 'testing', 'taskscomplete']")):
      ['getResponsiblePerson', 'review_state', 'portal_type', 'allowedRolesAndUsers'],
    ('allowedRolesAndUsers', 'path', ('portal_type', "'ExtropyActivity'"), ('review_state', "['open', 'in-progress', 'active', 'unassigned', 'deferred', 'assigned', 'testing', 'taskscomplete']")):
      ['path', 'review_state', 'portal_type', 'allowedRolesAndUsers'],
    ('allowedRolesAndUsers', 'path', ('portal_type', "'ExtropyPhase'"), ('review_state', "'active'")):
      ['path', 'review_state', 'portal_type', 'allowedRolesAndUsers'],
    ('allowedRolesAndUsers', 'sort_on', ('meta_type', "'ExtropyProject'"), ('review_state', "['active', 'closable']")):
      ['meta_type', 'review_state', 'allowedRolesAndUsers'],
    ('allowedRolesAndUsers', ('portal_type', "'ExtropyPhase'"), ('review_state', "['active', 'prospective', 'closable']")):
      ['review_state', 'portal_type', 'allowedRolesAndUsers'],
  },
  '/intranet.psol/extropy_tracking_tool:valueindexes': frozenset([
    'meta_type',
    'portal_type',
    'review_state',
  ]),
  '/intranet.psol/extropy_timetracker_tool': {
    ('Creator', 'allowedRolesAndUsers', 'path', 'portal_type', 'sort_on', 'sort_order', 'start'):
      ['path', 'start', 'Creator', 'allowedRolesAndUsers', 'portal_type'],
    ('Creator', 'allowedRolesAndUsers', 'path', 'portal_type', 'sort_on', 'start'):
      ['path', 'start', 'Creator', 'allowedRolesAndUsers', 'portal_type'],
    ('allowedRolesAndUsers', 'path', 'portal_type', 'sort_on'):
      ['path', 'allowedRolesAndUsers', 'portal_type'],
    ('allowedRolesAndUsers', 'path', 'portal_type', 'sort_on', 'sort_order', 'start'):
      ['path', 'start', 'allowedRolesAndUsers', 'portal_type'],
    ('allowedRolesAndUsers', 'path', 'portal_type', 'sort_on', 'start'):
      ['path', 'start', 'allowedRolesAndUsers', 'portal_type'],
    ('allowedRolesAndUsers', 'path', 'portal_type', 'sort_on', ('getBudgetCategory', "'Billable'"), ('review_state', "'entered'")):
      ['path', 'review_state', 'getBudgetCategory', 'allowedRolesAndUsers', 'portal_type'],
  },
  '/intranet.psol/extropy_timetracker_tool:valueindexes': frozenset([
    'getBudgetCategory',
    'review_state',
  ]),
}
