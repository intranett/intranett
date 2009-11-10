# query plan dumped at 'Tue Nov 10 16:27:47 2009'

queryplan = {
  '/intranet.psol/portal_catalog': {
    ('SearchableText', 'allowedRolesAndUsers', 'effectiveRange', 'path', ('portal_type', "['ATFile', 'Document', 'Event', 'ExtropyActivity', 'ExtropyFeature', 'ExtropyPhase', 'ExtropyProject', 'Favorite', 'File', 'Folder', 'GeoLocation', 'Image', 'Invoice', 'Large Plone Folder', 'Link', 'Memo', 'News Item', 'Topic']")):
      ['SearchableText', 'allowedRolesAndUsers', 'portal_type', 'effectiveRange', 'path'],
    ('SearchableText', 'allowedRolesAndUsers', 'path', 'show_inactive', ('portal_type', "['ATFile', 'Document', 'Event', 'ExtropyActivity', 'ExtropyFeature', 'ExtropyPhase', 'ExtropyProject', 'Favorite', 'File', 'Folder', 'GeoLocation', 'Image', 'Invoice', 'Large Plone Folder', 'Link', 'Memo', 'News Item', 'Topic']")):
      ['SearchableText', 'portal_type', 'path', 'allowedRolesAndUsers'],
    ('SearchableText', 'allowedRolesAndUsers', 'path', ('portal_type', "['ATFile', 'Document', 'Event', 'ExtropyActivity', 'ExtropyFeature', 'ExtropyPhase', 'ExtropyProject', 'Favorite', 'File', 'Folder', 'GeoLocation', 'Image', 'Invoice', 'Large Plone Folder', 'Link', 'Memo', 'News Item', 'Topic']")):
      ['SearchableText', 'portal_type', 'path', 'allowedRolesAndUsers'],
    ('allowedRolesAndUsers', 'effectiveRange', 'path', 'sort_on', 'sort_order', ('is_default_page', 'False'), ('is_folderish', 'True'), ('portal_type', "['ATFile', 'ExtropyActivity', 'ExtropyPhase', 'ExtropyProject', 'Folder', 'Large Plone Folder', 'Memo', 'Topic']"), ('review_state', "('Sent', 'active', 'prospective', 'open', 'assigned', 'entered', 'external', 'internal', 'internally_published', 'pending', 'planned', 'private', 'prospective', 'Draft', 'published', 'testing', 'unassigned')")):
      ['allowedRolesAndUsers', 'path', 'portal_type', 'review_state', 'is_folderish', 'is_default_page', 'effectiveRange'],
    ('allowedRolesAndUsers', 'effectiveRange', 'path', 'sort_on', 'sort_order', ('is_default_page', 'False'), ('portal_type', "['ATFile', 'ExtropyActivity', 'ExtropyPhase', 'ExtropyProject', 'Folder', 'Large Plone Folder', 'Memo', 'Topic']"), ('review_state', "('Sent', 'active', 'prospective', 'open', 'assigned', 'entered', 'external', 'internal', 'internally_published', 'pending', 'planned', 'private', 'prospective', 'Draft', 'published', 'testing', 'unassigned')")):
      ['allowedRolesAndUsers', 'path', 'portal_type', 'review_state', 'is_default_page', 'effectiveRange'],
    ('allowedRolesAndUsers', 'path', 'show_inactive', 'sort_on'):
      ['path', 'allowedRolesAndUsers'],
    ('allowedRolesAndUsers', 'path', 'sort_on', 'sort_order', ('is_default_page', 'False'), ('is_folderish', 'True'), ('portal_type', "['ATFile', 'ExtropyActivity', 'ExtropyPhase', 'ExtropyProject', 'Folder', 'Large Plone Folder', 'Memo', 'Topic']"), ('review_state', "('Sent', 'active', 'prospective', 'open', 'assigned', 'entered', 'external', 'internal', 'internally_published', 'pending', 'planned', 'private', 'prospective', 'Draft', 'published', 'testing', 'unassigned')")):
      ['path', 'portal_type', 'review_state', 'is_folderish', 'is_default_page', 'allowedRolesAndUsers'],
    ('allowedRolesAndUsers', 'path', 'sort_on', 'sort_order', ('is_default_page', 'False'), ('portal_type', "['ATFile', 'ExtropyActivity', 'ExtropyPhase', 'ExtropyProject', 'Folder', 'Large Plone Folder', 'Memo', 'Topic']"), ('review_state', "('Sent', 'active', 'prospective', 'open', 'assigned', 'entered', 'external', 'internal', 'internally_published', 'pending', 'planned', 'private', 'prospective', 'Draft', 'published', 'testing', 'unassigned')")):
      ['path', 'portal_type', 'review_state', 'is_default_page', 'allowedRolesAndUsers'],
    ('allowedRolesAndUsers', 'sort_on', 'sort_order'):
      ['allowedRolesAndUsers'],
    ('allowedRolesAndUsers', ('review_state', "['pending']")):
      ['review_state', 'allowedRolesAndUsers'],
    ('path',):
      ['path'],
  },
  '/intranet.psol/reference_catalog': {
    ('merge', 'sourceUID', ('relationship', "'relatesTo'")):
      ['sourceUID', 'relationship'],
  },
  '/intranet.psol/extropy_tracking_tool': {
    ('allowedRolesAndUsers', 'getParticipants', ('portal_type', "'ExtropyProject'"), ('review_state', "'active'")):
      ['getParticipants', 'portal_type', 'review_state', 'allowedRolesAndUsers'],
    ('allowedRolesAndUsers', 'getResponsiblePerson', 'path', 'sort_on', ('portal_type', "['ExtropyTask', 'ExtropyActivity', 'ExtropyFeature']"), ('review_state', "['open', 'in-progress', 'active', 'unassigned', 'deferred', 'assigned', 'testing', 'taskscomplete']")):
      ['path', 'getResponsiblePerson', 'review_state', 'portal_type', 'allowedRolesAndUsers'],
    ('allowedRolesAndUsers', 'getResponsiblePerson', ('portal_type', "('ExtropyActivity', 'ExtropyFeature', 'ExtropyTask')"), ('review_state', "['open', 'in-progress', 'active', 'unassigned', 'deferred', 'assigned', 'testing', 'taskscomplete']")):
      ['getResponsiblePerson', 'review_state', 'portal_type', 'allowedRolesAndUsers'],
    ('allowedRolesAndUsers', 'sort_on', ('meta_type', "'ExtropyProject'"), ('review_state', "['active', 'closable']")):
      ['meta_type', 'review_state', 'allowedRolesAndUsers'],
  },
  '/intranet.psol/extropy_timetracker_tool': {
    ('path', 'sort_on', 'sort_order', 'start', ('allowedRolesAndUsers', "['Manager', 'Authenticated', 'Anonymous', 'user:root']"), ('portal_type', "'ExtropyHours'")):
      ['path', 'start', 'allowedRolesAndUsers', 'portal_type'],
    ('path', 'sort_on', 'start', ('Creator', "'chris'"), ('allowedRolesAndUsers', "['Manager', 'Authenticated', 'Anonymous', 'user:root']"), ('portal_type', "'ExtropyHours'")):
      ['path', 'start', 'Creator', 'allowedRolesAndUsers', 'portal_type'],
    ('path', 'sort_on', 'start', ('Creator', "'hannosch'"), ('allowedRolesAndUsers', "['Manager', 'Authenticated', 'Anonymous', 'user:root']"), ('portal_type', "'ExtropyHours'")):
      ['path', 'start', 'Creator', 'allowedRolesAndUsers', 'portal_type'],
    ('path', 'sort_on', 'start', ('Creator', "'root'"), ('allowedRolesAndUsers', "['Manager', 'Authenticated', 'Anonymous', 'user:root']"), ('portal_type', "'ExtropyHours'")):
      ['path', 'Creator', 'start', 'allowedRolesAndUsers', 'portal_type'],
    ('path', 'sort_on', 'start', ('allowedRolesAndUsers', "['Manager', 'Authenticated', 'Anonymous', 'user:root']"), ('portal_type', "'ExtropyHours'")):
      ['path', 'start', 'allowedRolesAndUsers', 'portal_type'],
    ('start', ('allowedRolesAndUsers', "['Manager', 'Authenticated', 'Anonymous', 'user:root']"), ('getBudgetCategory', "'Billable'"), ('portal_type', "'ExtropyHours'")):
      ['start', 'getBudgetCategory', 'allowedRolesAndUsers', 'portal_type'],
    ('start', ('allowedRolesAndUsers', "['Manager', 'Authenticated', 'Anonymous', 'user:root']"), ('portal_type', "'ExtropyHours'")):
      ['start', 'allowedRolesAndUsers', 'portal_type'],
  },
}
