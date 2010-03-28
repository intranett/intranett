# query plan dumped at 'Sun Mar 28 14:27:10 2010'

queryplan = {
  '/intranet.psol/portal_catalog': {
    ('Creator', 'allowedRolesAndUsers', 'sort_on', 'sort_order'):
      ['Creator', 'allowedRolesAndUsers'],
    ('SearchableText', 'allowedRolesAndUsers', 'effectiveRange', 'path', 'sort_limit', ('portal_type', "['ATFile', 'ATImage', 'Document', 'ExtropyActivity', 'ExtropyFeature', 'ExtropyPhase', 'ExtropyProject', 'File', 'Folder', 'GeoLocation', 'Image', 'Invoice', 'Large Plone Folder', 'Link', 'Topic']")):
      ['SearchableText', 'allowedRolesAndUsers', 'portal_type', 'effectiveRange', 'path'],
    ('SearchableText', 'allowedRolesAndUsers', 'effectiveRange', 'path', 'sort_limit', ('portal_type', "['ATFile', 'Document', 'ExtropyActivity', 'ExtropyFeature', 'ExtropyPhase', 'ExtropyProject', 'File', 'Folder', 'GeoLocation', 'Image', 'Invoice', 'Large Plone Folder', 'Link', 'Topic']")):
      ['SearchableText', 'allowedRolesAndUsers', 'portal_type', 'effectiveRange', 'path'],
    ('SearchableText', 'allowedRolesAndUsers', 'path', 'show_inactive', ('portal_type', "['ATFile', 'ATImage', 'Document', 'ExtropyActivity', 'ExtropyFeature', 'ExtropyPhase', 'ExtropyProject', 'File', 'Folder', 'GeoLocation', 'Image', 'Invoice', 'Large Plone Folder', 'Link', 'Topic']")):
      ['SearchableText', 'portal_type', 'allowedRolesAndUsers', 'path'],
    ('SearchableText', 'allowedRolesAndUsers', 'path', 'show_inactive', ('portal_type', "['ATFile', 'Document', 'ExtropyActivity', 'ExtropyFeature', 'ExtropyPhase', 'ExtropyProject', 'File', 'Folder', 'GeoLocation', 'Image', 'Invoice', 'Large Plone Folder', 'Link', 'Topic']")):
      ['SearchableText', 'portal_type', 'path', 'allowedRolesAndUsers'],
    ('SearchableText', 'allowedRolesAndUsers', 'path', ('portal_type', "['ATFile', 'ATImage', 'Document', 'ExtropyActivity', 'ExtropyFeature', 'ExtropyPhase', 'ExtropyProject', 'File', 'Folder', 'GeoLocation', 'Image', 'Invoice', 'Large Plone Folder', 'Link', 'Topic']")):
      ['SearchableText', 'portal_type', 'allowedRolesAndUsers', 'path'],
    ('SearchableText', 'allowedRolesAndUsers', 'path', ('portal_type', "['ATFile', 'Document', 'ExtropyActivity', 'ExtropyFeature', 'ExtropyPhase', 'ExtropyProject', 'File', 'Folder', 'GeoLocation', 'Image', 'Invoice', 'Large Plone Folder', 'Link', 'Topic']")):
      ['SearchableText', 'portal_type', 'path', 'allowedRolesAndUsers'],
    ('SearchableText', 'allowedRolesAndUsers', 'show_inactive', 'sort_on', 'sort_order', ('portal_type', "['ATFile', 'ATImage', 'Document', 'ExtropyActivity', 'ExtropyFeature', 'ExtropyPhase', 'ExtropyProject', 'File', 'Folder', 'GeoLocation', 'Image', 'Invoice', 'Large Plone Folder', 'Link', 'Topic']")):
      ['SearchableText', 'portal_type', 'allowedRolesAndUsers'],
    ('Title', 'allowedRolesAndUsers', 'sort_on', 'sort_order'):
      ['Title', 'allowedRolesAndUsers'],
    ('Type', 'allowedRolesAndUsers', 'path'):
      ['Type', 'path', 'allowedRolesAndUsers'],
    ('Type', 'allowedRolesAndUsers', 'sort_on', 'sort_order'):
      ['Type', 'allowedRolesAndUsers'],
    ('allowedRolesAndUsers', 'effectiveRange', 'path', 'sort_on', 'sort_order', ('is_default_page', 'False'), ('is_folderish', 'True'), ('portal_type', "['ATFile', 'ATImage', 'ExtropyActivity', 'ExtropyPhase', 'ExtropyProject', 'Folder', 'Large Plone Folder', 'Topic']"), ('review_state', "('Sent', 'active', 'prospective', 'open', 'assigned', 'entered', 'external', 'internal', 'internally_published', 'pending', 'planned', 'private', 'prospective', 'Draft', 'published', 'testing', 'unassigned')")):
      ['allowedRolesAndUsers', 'path', 'portal_type', 'is_folderish', 'review_state', 'is_default_page', 'effectiveRange'],
    ('allowedRolesAndUsers', 'effectiveRange', 'path', 'sort_on', 'sort_order', ('is_default_page', 'False'), ('is_folderish', 'True'), ('portal_type', "['ATFile', 'ExtropyActivity', 'ExtropyPhase', 'ExtropyProject', 'Folder', 'Large Plone Folder', 'Topic']"), ('review_state', "('Sent', 'active', 'prospective', 'open', 'assigned', 'entered', 'external', 'internal', 'internally_published', 'pending', 'planned', 'private', 'prospective', 'Draft', 'published', 'testing', 'unassigned')")):
      ['allowedRolesAndUsers', 'path', 'portal_type', 'review_state', 'is_folderish', 'is_default_page', 'effectiveRange'],
    ('allowedRolesAndUsers', 'effectiveRange', 'path', 'sort_on', 'sort_order', ('is_default_page', 'False'), ('portal_type', "['ATFile', 'ATImage', 'ExtropyActivity', 'ExtropyPhase', 'ExtropyProject', 'Folder', 'Large Plone Folder', 'Topic']"), ('review_state', "('Sent', 'active', 'prospective', 'open', 'assigned', 'entered', 'external', 'internal', 'internally_published', 'pending', 'planned', 'private', 'prospective', 'Draft', 'published', 'testing', 'unassigned')")):
      ['allowedRolesAndUsers', 'path', 'portal_type', 'review_state', 'is_default_page', 'effectiveRange'],
    ('allowedRolesAndUsers', 'effectiveRange', 'path', 'sort_on', 'sort_order', ('is_default_page', 'False'), ('portal_type', "['ATFile', 'ExtropyActivity', 'ExtropyPhase', 'ExtropyProject', 'Folder', 'Large Plone Folder', 'Topic']"), ('review_state', "('Sent', 'active', 'prospective', 'open', 'assigned', 'entered', 'external', 'internal', 'internally_published', 'pending', 'planned', 'private', 'prospective', 'Draft', 'published', 'testing', 'unassigned')")):
      ['allowedRolesAndUsers', 'path', 'portal_type', 'review_state', 'is_default_page', 'effectiveRange'],
    ('allowedRolesAndUsers', 'end', 'path', 'sort_limit', 'sort_on', ('portal_type', "'Event'"), ('review_state', "('published',)")):
      ['end', 'portal_type', 'review_state', 'path', 'allowedRolesAndUsers'],
    ('allowedRolesAndUsers', 'path'):
      ['path', 'allowedRolesAndUsers'],
    ('allowedRolesAndUsers', 'path', 'show_inactive', 'sort_on'):
      ['path', 'allowedRolesAndUsers'],
    ('allowedRolesAndUsers', 'path', 'show_inactive', 'sort_on', ('portal_type', "['Image', 'Document', 'Event', 'File', 'Invoice', 'ExtropyActivity']")):
      ['path', 'portal_type', 'allowedRolesAndUsers'],
    ('allowedRolesAndUsers', 'path', 'show_inactive', 'sort_on', ('portal_type', "['Image', 'Document', 'Event', 'File']")):
      ['path', 'portal_type', 'allowedRolesAndUsers'],
    ('allowedRolesAndUsers', 'path', 'show_inactive', 'sort_on', ('portal_type', "['Image', 'Document', 'Event', 'Folder', 'File', 'Invoice']")):
      ['path', 'portal_type', 'allowedRolesAndUsers'],
    ('allowedRolesAndUsers', 'path', 'sort_limit', 'sort_on', 'sort_order', ('portal_type', "'News Item'"), ('review_state', "('published',)")):
      ['portal_type', 'review_state', 'path', 'allowedRolesAndUsers'],
    ('allowedRolesAndUsers', 'path', 'sort_limit', 'sort_on', 'sort_order', ('portal_type', "['ATFile', 'Document', 'ExtropyActivity', 'ExtropyFeature', 'ExtropyPhase', 'ExtropyProject', 'File', 'Folder', 'GeoLocation', 'Image', 'Invoice', 'Large Plone Folder', 'Link', 'Topic']")):
      ['portal_type', 'path', 'allowedRolesAndUsers'],
    ('allowedRolesAndUsers', 'path', 'sort_on', 'sort_order'):
      ['path', 'allowedRolesAndUsers'],
    ('allowedRolesAndUsers', 'path', 'sort_on', 'sort_order', ('is_default_page', 'False'), ('is_folderish', 'True'), ('portal_type', "['ATFile', 'ATImage', 'ExtropyActivity', 'ExtropyPhase', 'ExtropyProject', 'Folder', 'Large Plone Folder', 'Topic']"), ('review_state', "('Sent', 'active', 'prospective', 'open', 'assigned', 'entered', 'external', 'internal', 'internally_published', 'pending', 'planned', 'private', 'prospective', 'Draft', 'published', 'testing', 'unassigned')")):
      ['path', 'portal_type', 'is_folderish', 'review_state', 'is_default_page', 'allowedRolesAndUsers'],
    ('allowedRolesAndUsers', 'path', 'sort_on', 'sort_order', ('is_default_page', 'False'), ('is_folderish', 'True'), ('portal_type', "['ATFile', 'ExtropyActivity', 'ExtropyPhase', 'ExtropyProject', 'Folder', 'Large Plone Folder', 'Topic']"), ('review_state', "('Sent', 'active', 'prospective', 'open', 'assigned', 'entered', 'external', 'internal', 'internally_published', 'pending', 'planned', 'private', 'prospective', 'Draft', 'published', 'testing', 'unassigned')")):
      ['path', 'portal_type', 'review_state', 'is_folderish', 'is_default_page', 'allowedRolesAndUsers'],
    ('allowedRolesAndUsers', 'path', 'sort_on', 'sort_order', ('is_default_page', 'False'), ('portal_type', "['ATFile', 'ATImage', 'ExtropyActivity', 'ExtropyPhase', 'ExtropyProject', 'Folder', 'Large Plone Folder', 'Topic']"), ('review_state', "('Sent', 'active', 'prospective', 'open', 'assigned', 'entered', 'external', 'internal', 'internally_published', 'pending', 'planned', 'private', 'prospective', 'Draft', 'published', 'testing', 'unassigned')")):
      ['path', 'portal_type', 'review_state', 'is_default_page', 'allowedRolesAndUsers'],
    ('allowedRolesAndUsers', 'path', 'sort_on', 'sort_order', ('is_default_page', 'False'), ('portal_type', "['ATFile', 'ExtropyActivity', 'ExtropyPhase', 'ExtropyProject', 'Folder', 'Large Plone Folder', 'Topic']"), ('review_state', "('Sent', 'active', 'prospective', 'open', 'assigned', 'entered', 'external', 'internal', 'internally_published', 'pending', 'planned', 'private', 'prospective', 'Draft', 'published', 'testing', 'unassigned')")):
      ['path', 'portal_type', 'review_state', 'is_default_page', 'allowedRolesAndUsers'],
    ('allowedRolesAndUsers', 'path', 'sort_on', ('portal_type', "'Invoice'")):
      ['path', 'portal_type', 'allowedRolesAndUsers'],
    ('allowedRolesAndUsers', 'path', ('Type', "'Invoice'")):
      ['Type', 'allowedRolesAndUsers', 'path'],
    ('allowedRolesAndUsers', 'sort_on', 'sort_order'):
      ['allowedRolesAndUsers'],
    ('allowedRolesAndUsers', 'sort_on', 'sort_order', ('Type', "'Invoice'")):
      ['Type', 'allowedRolesAndUsers'],
    ('allowedRolesAndUsers', ('portal_type', "['ATFile', 'ChangeSet', 'Document', 'ExtropyBug', 'ExtropyHourGlass', 'ExtropyJar', 'ExtropyTaskHistory', 'Favorite', 'File', 'Folder', 'GeoLocation', 'Image', 'Large Plone Folder', 'Link', 'News Item', 'TempFolder', 'Topic']"), ('review_state', "('pending',)")):
      ['review_state', 'portal_type', 'allowedRolesAndUsers'],
    ('allowedRolesAndUsers', ('portal_type', "['Document', 'Event', 'File', 'Image', 'Link', 'News Item']"), ('review_state', "('pending',)")):
      ['review_state', 'portal_type', 'allowedRolesAndUsers'],
    ('allowedRolesAndUsers', ('portal_type', "['Document', 'Event', 'Folder', 'Large Plone Folder', 'Link', 'News Item', 'Topic']"), ('review_state', "('pending',)")):
      ['review_state', 'portal_type', 'allowedRolesAndUsers'],
    ('allowedRolesAndUsers', ('portal_type', "['Event', 'Memo']"), ('review_state', "('pending',)")):
      ['review_state', 'portal_type', 'allowedRolesAndUsers'],
    ('allowedRolesAndUsers', ('portal_type', "['ExtropyActivity', 'ExtropyPhase', 'ExtropyProject']"), ('review_state', "('pending',)")):
      ['review_state', 'portal_type', 'allowedRolesAndUsers'],
    ('allowedRolesAndUsers', ('portal_type', "['ExtropyFeature']"), ('review_state', "('pending',)")):
      ['review_state', 'portal_type', 'allowedRolesAndUsers'],
    ('allowedRolesAndUsers', ('portal_type', "['ExtropyTask']"), ('review_state', "('pending',)")):
      ['review_state', 'portal_type', 'allowedRolesAndUsers'],
    ('allowedRolesAndUsers', ('portal_type', "['Folder', 'Large Plone Folder', 'Topic']"), ('review_state', "('pending',)")):
      ['review_state', 'portal_type', 'allowedRolesAndUsers'],
    ('allowedRolesAndUsers', ('portal_type', "['Invoice']"), ('review_state', "('pending',)")):
      ['review_state', 'portal_type', 'allowedRolesAndUsers'],
    ('allowedRolesAndUsers', ('review_state', "['pending']")):
      ['review_state', 'allowedRolesAndUsers'],
    ('path',):
      ['path'],
  },
  '/intranet.psol/portal_catalog:valueindexes': frozenset([
    'Type',
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
    ('merge', 'targetUID', ('relationship', "'invoice'")):
      ['targetUID', 'relationship'],
    ('sourceUID', ('relationship', "'relatesTo'")):
      ['sourceUID', 'relationship'],
  },
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
    ('allowedRolesAndUsers', 'getResponsiblePerson', 'path', ('portal_type', "['ExtropyTask', 'ExtropyActivity', 'ExtropyFeature']"), ('review_state', "['open', 'in-progress', 'active', 'unassigned', 'deferred', 'assigned', 'testing', 'taskscomplete']")):
      ['path', 'getResponsiblePerson', 'review_state', 'portal_type', 'allowedRolesAndUsers'],
    ('allowedRolesAndUsers', 'getResponsiblePerson', ('portal_type', "('ExtropyActivity', 'ExtropyFeature', 'ExtropyTask')"), ('review_state', "['open', 'in-progress', 'active', 'unassigned', 'deferred', 'assigned', 'testing', 'taskscomplete']")):
      ['getResponsiblePerson', 'review_state', 'portal_type', 'allowedRolesAndUsers'],
    ('allowedRolesAndUsers', 'path', ('meta_type', "'ExtropyActivity'")):
      ['path', 'meta_type', 'allowedRolesAndUsers'],
    ('allowedRolesAndUsers', 'path', ('meta_type', "'ExtropyTask'")):
      ['path', 'meta_type', 'allowedRolesAndUsers'],
    ('allowedRolesAndUsers', 'path', ('portal_type', "'ExtropyActivity'"), ('review_state', "['open', 'in-progress', 'active', 'unassigned', 'deferred', 'assigned', 'testing', 'taskscomplete']")):
      ['path', 'review_state', 'portal_type', 'allowedRolesAndUsers'],
    ('allowedRolesAndUsers', 'path', ('portal_type', "'ExtropyFeature'"), ('review_state', "['open', 'in-progress', 'active', 'unassigned', 'deferred', 'assigned', 'testing', 'taskscomplete']")):
      ['path', 'review_state', 'portal_type', 'allowedRolesAndUsers'],
    ('allowedRolesAndUsers', 'path', ('portal_type', "'ExtropyPhase'"), ('review_state', "'active'")):
      ['path', 'review_state', 'portal_type', 'allowedRolesAndUsers'],
    ('allowedRolesAndUsers', 'path', ('portal_type', "'ExtropyTask'")):
      ['path', 'portal_type', 'allowedRolesAndUsers'],
    ('allowedRolesAndUsers', 'path', ('portal_type', "'ExtropyTask'"), ('review_state', "['open', 'in-progress', 'active', 'unassigned', 'deferred', 'assigned', 'testing', 'taskscomplete']")):
      ['path', 'review_state', 'portal_type', 'allowedRolesAndUsers'],
    ('allowedRolesAndUsers', 'sort_on', ('meta_type', "'ExtropyProject'"), ('review_state', "['active', 'closable']")):
      ['meta_type', 'review_state', 'allowedRolesAndUsers'],
    ('allowedRolesAndUsers', ('portal_type', "'ExtropyPhase'"), ('review_state', "['active', 'prospective', 'closable']")):
      ['review_state', 'portal_type', 'allowedRolesAndUsers'],
    ('path',):
      ['path'],
  },
  '/intranet.psol/extropy_tracking_tool:valueindexes': frozenset([
    'meta_type',
    'portal_type',
    'review_state',
  ]),
  '/intranet.psol/extropy_timetracker_tool': {
    ('path',):
      ['path'],
  },
  '/intranet.psol/extropy_timetracker_tool:valueindexes': frozenset([
    'getBudgetCategory',
    'review_state',
  ]),
}
