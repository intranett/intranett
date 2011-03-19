# query plan dumped at 'Mon Feb 14 16:16:46 2011'

queryplan = {
  '/Plone/portal_catalog': {
    ('SearchableText', 'effectiveRange', 'path', 'sort_limit', ('allowedRolesAndUsers', "['Anonymous', 'Anonymous', 'user:None']"), ('portal_type', "['Document', 'Event', 'File', 'Folder', 'FormFolder', 'Image', 'Link', 'MemberData', 'News Item', 'Topic']")):
      ['SearchableText', 'allowedRolesAndUsers', 'portal_type', 'effectiveRange', 'path'],
    ('SearchableText', 'path', 'sort_limit', ('allowedRolesAndUsers', "['Manager', 'Authenticated', 'Anonymous', 'user:admin']"), ('portal_type', "['Document', 'Event', 'File', 'Folder', 'FormFolder', 'Image', 'Link', 'MemberData', 'News Item', 'Topic']")):
      ['SearchableText', 'portal_type', 'allowedRolesAndUsers', 'path'],
    ('effectiveRange', 'path', 'sort_on', 'sort_order', ('allowedRolesAndUsers', "['Anonymous', 'Anonymous', 'user:None']"), ('is_default_page', 'False'), ('is_folderish', 'True'), ('portal_type', "['Document', 'Folder', 'Image', 'MemberData', 'News Item']")):
      ['is_folderish', 'path', 'allowedRolesAndUsers', 'portal_type', 'is_default_page', 'effectiveRange'],
    ('end', 'path', 'sort_limit', 'sort_on', ('allowedRolesAndUsers', "['Manager', 'Authenticated', 'Anonymous', 'user:admin']"), ('portal_type', "'Event'"), ('review_state', "('published',)")):
      ['end', 'portal_type', 'review_state', 'allowedRolesAndUsers', 'path'],
    ('path',):
      ['path'],
    ('path', 'show_inactive', 'sort_on', ('allowedRolesAndUsers', "['Manager', 'Authenticated', 'Anonymous', 'user:admin']")):
      ['path', 'allowedRolesAndUsers'],
    ('path', 'sort_limit', 'sort_on', 'sort_order', ('allowedRolesAndUsers', "['Manager', 'Authenticated', 'Anonymous', 'user:admin']"), ('portal_type', "'News Item'"), ('review_state', "('published',)")):
      ['portal_type', 'review_state', 'allowedRolesAndUsers', 'path'],
    ('path', 'sort_on', 'sort_order', ('allowedRolesAndUsers', "['Manager', 'Authenticated', 'Anonymous', 'user:admin']"), ('is_default_page', 'False'), ('is_folderish', 'True'), ('portal_type', "['Document', 'Folder', 'Image', 'MemberData', 'News Item']")):
      ['is_folderish', 'path', 'portal_type', 'is_default_page', 'allowedRolesAndUsers'],
    ('path', 'sort_on', 'sort_order', ('allowedRolesAndUsers', "['Manager', 'Authenticated', 'Anonymous', 'user:admin']"), ('is_default_page', 'False'), ('portal_type', "['Document', 'Event', 'File', 'Folder', 'FormFolder', 'Image', 'Large Plone Folder', 'Link', 'News Item', 'Topic']")):
      ['path', 'allowedRolesAndUsers', 'is_default_page', 'portal_type'],
    ('path', 'sort_on', 'sort_order', ('allowedRolesAndUsers', "['Manager', 'Authenticated', 'Anonymous', 'user:admin']"), ('is_default_page', 'False'), ('portal_type', "['Document', 'Event', 'File', 'Folder', 'FormFolder', 'Image', 'Link', 'MemberData', 'News Item', 'Topic']")):
      ['path', 'portal_type', 'is_default_page', 'allowedRolesAndUsers'],
    ('path', 'sort_on', 'sort_order', ('allowedRolesAndUsers', "['Manager', 'Authenticated', 'Anonymous', 'user:admin']"), ('is_default_page', 'False'), ('portal_type', "['Document', 'Folder']")):
      ['path', 'allowedRolesAndUsers', 'is_default_page', 'portal_type'],
  },
  '/Plone/portal_catalog:valueindexes': frozenset([
    'Subject',
    'Type',
    'allowedRolesAndUsers',
    'is_default_page',
    'is_folderish',
    'meta_type',
    'object_provides',
    'portal_type',
    'review_state',
  ]),
  '/Plone/reference_catalog': {
    ('merge', 'sourceUID', ('relationship', "'isReferencing'")):
      ['relationship', 'sourceUID'],
    ('merge', 'sourceUID', ('relationship', "'relatesTo'")):
      ['relationship', 'sourceUID'],
    ('sourceUID', ('relationship', "'relatesTo'")):
      ['relationship', 'sourceUID'],
  },
  '/Plone/reference_catalog:valueindexes': frozenset([
    'relationship',
  ]),
  '/intranet.psol/portal_catalog': {
    ('allowedRolesAndUsers', 'effectiveRange', 'path', 'show_inactive', 'sort_on'):
      ['allowedRolesAndUsers', 'path', 'effectiveRange'],
    ('allowedRolesAndUsers', 'effectiveRange', 'path', 'sort_on', 'sort_order', ('is_default_page', 'False'), ('is_folderish', 'True'), ('portal_type', "['ExtropyActivity', 'ExtropyPhase', 'ExtropyProject', 'Folder', 'Topic']"), ('review_state', "('Sent', 'active', 'prospective', 'open', 'assigned', 'entered', 'external', 'internal', 'internally_published', 'pending', 'planned', 'private', 'prospective', 'Draft', 'published', 'testing', 'unassigned')")):
      ['allowedRolesAndUsers', 'path', 'portal_type', 'is_folderish', 'review_state', 'is_default_page', 'effectiveRange'],
    ('allowedRolesAndUsers', 'effectiveRange', 'path', 'sort_on', 'sort_order', ('is_default_page', 'False'), ('portal_type', "['ATFile', 'ATImage', 'ExtropyActivity', 'ExtropyPhase', 'ExtropyProject', 'Folder', 'Large Plone Folder', 'Topic']"), ('review_state', "('Sent', 'active', 'prospective', 'open', 'assigned', 'entered', 'external', 'internal', 'internally_published', 'pending', 'planned', 'private', 'prospective', 'Draft', 'published', 'testing', 'unassigned')")):
      ['allowedRolesAndUsers', 'path', 'portal_type', 'review_state', 'is_default_page', 'effectiveRange'],
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
    ('UID', 'allowedRolesAndUsers'):
      ['UID', 'allowedRolesAndUsers'],
    ('allowedRolesAndUsers', 'effectiveRange', 'getParticipants', ('portal_type', "'ExtropyProject'"), ('review_state', "'active'")):
      ['allowedRolesAndUsers', 'getParticipants', 'portal_type', 'review_state'],
    ('allowedRolesAndUsers', 'effectiveRange', 'getResponsiblePerson', ('portal_type', "('ExtropyActivity', 'ExtropyFeature', 'ExtropyTask')"), ('review_state', "['open', 'in-progress', 'active', 'unassigned', 'deferred', 'assigned', 'testing', 'taskscomplete']")):
      ['allowedRolesAndUsers', 'getResponsiblePerson', 'review_state', 'portal_type'],
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
    ('Creator', 'allowedRolesAndUsers', 'portal_type', 'sort_on', 'start'):
      ['start', 'Creator', 'allowedRolesAndUsers', 'portal_type'],
    ('allowedRolesAndUsers', 'path', 'portal_type', 'sort_on'):
      ['path', 'allowedRolesAndUsers', 'portal_type'],
    ('allowedRolesAndUsers', 'path', 'portal_type', 'sort_on', 'sort_order', 'start'):
      ['path', 'start', 'allowedRolesAndUsers', 'portal_type'],
    ('allowedRolesAndUsers', 'path', 'portal_type', 'sort_on', 'start'):
      ['path', 'start', 'allowedRolesAndUsers', 'portal_type'],
    ('allowedRolesAndUsers', 'path', 'portal_type', 'sort_on', ('getBudgetCategory', "'Billable'"), ('review_state', "'entered'")):
      ['path', 'review_state', 'getBudgetCategory', 'allowedRolesAndUsers', 'portal_type'],
    ('path',):
      ['path'],
  },
  '/intranet.psol/extropy_timetracker_tool:valueindexes': frozenset([
    'getBudgetCategory',
    'review_state',
  ]),
}
