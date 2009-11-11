# query plan dumped at 'Wed Nov 11 16:27:01 2009'

queryplan = {
  '/intranet.psol/portal_catalog': {
    ('SearchableText', 'allowedRolesAndUsers', 'path', 'show_inactive', ('portal_type', "['ATFile', 'Document', 'ExtropyActivity', 'ExtropyFeature', 'ExtropyPhase', 'ExtropyProject', 'File', 'Folder', 'GeoLocation', 'Image', 'Invoice', 'Large Plone Folder', 'Link', 'Topic']")):
      ['SearchableText', 'portal_type', 'path', 'allowedRolesAndUsers'],
    ('SearchableText', 'allowedRolesAndUsers', 'path', ('portal_type', "['ATFile', 'Document', 'ExtropyActivity', 'ExtropyFeature', 'ExtropyPhase', 'ExtropyProject', 'File', 'Folder', 'GeoLocation', 'Image', 'Invoice', 'Large Plone Folder', 'Link', 'Topic']")):
      ['SearchableText', 'portal_type', 'path', 'allowedRolesAndUsers'],
    ('Type', 'allowedRolesAndUsers', 'path'):
      ['Type', 'path', 'allowedRolesAndUsers'],
    ('Type', 'allowedRolesAndUsers', 'sort_on', 'sort_order'):
      ['Type', 'allowedRolesAndUsers'],
    ('allowedRolesAndUsers', 'effectiveRange', 'path', 'sort_on', 'sort_order', ('is_default_page', 'False'), ('is_folderish', 'True'), ('portal_type', "['ATFile', 'ExtropyActivity', 'ExtropyPhase', 'ExtropyProject', 'Folder', 'Large Plone Folder', 'Topic']"), ('review_state', "('Sent', 'active', 'prospective', 'open', 'assigned', 'entered', 'external', 'internal', 'internally_published', 'pending', 'planned', 'private', 'prospective', 'Draft', 'published', 'testing', 'unassigned')")):
      ['allowedRolesAndUsers', 'path', 'portal_type', 'review_state', 'is_folderish', 'is_default_page', 'effectiveRange'],
    ('allowedRolesAndUsers', 'effectiveRange', 'path', 'sort_on', 'sort_order', ('is_default_page', 'False'), ('portal_type', "['ATFile', 'ExtropyActivity', 'ExtropyPhase', 'ExtropyProject', 'Folder', 'Large Plone Folder', 'Topic']"), ('review_state', "('Sent', 'active', 'prospective', 'open', 'assigned', 'entered', 'external', 'internal', 'internally_published', 'pending', 'planned', 'private', 'prospective', 'Draft', 'published', 'testing', 'unassigned')")):
      ['allowedRolesAndUsers', 'path', 'portal_type', 'review_state', 'is_default_page', 'effectiveRange'],
    ('allowedRolesAndUsers', 'path', 'show_inactive', 'sort_on'):
      ['path', 'allowedRolesAndUsers'],
    ('allowedRolesAndUsers', 'path', 'show_inactive', 'sort_on', ('portal_type', "['Image', 'Document', 'Event', 'File', 'Invoice', 'ExtropyActivity']")):
      ['path', 'portal_type', 'allowedRolesAndUsers'],
    ('allowedRolesAndUsers', 'path', 'show_inactive', 'sort_on', ('portal_type', "['Image', 'Document', 'Event', 'Folder', 'File', 'Invoice']")):
      ['path', 'portal_type', 'allowedRolesAndUsers'],
    ('allowedRolesAndUsers', 'path', 'sort_on', 'sort_order', ('is_default_page', 'False'), ('is_folderish', 'True'), ('portal_type', "['ATFile', 'ExtropyActivity', 'ExtropyPhase', 'ExtropyProject', 'Folder', 'Large Plone Folder', 'Topic']"), ('review_state', "('Sent', 'active', 'prospective', 'open', 'assigned', 'entered', 'external', 'internal', 'internally_published', 'pending', 'planned', 'private', 'prospective', 'Draft', 'published', 'testing', 'unassigned')")):
      ['path', 'portal_type', 'review_state', 'is_folderish', 'is_default_page', 'allowedRolesAndUsers'],
    ('allowedRolesAndUsers', 'path', 'sort_on', 'sort_order', ('is_default_page', 'False'), ('portal_type', "['ATFile', 'ExtropyActivity', 'ExtropyPhase', 'ExtropyProject', 'Folder', 'Large Plone Folder', 'Topic']"), ('review_state', "('Sent', 'active', 'prospective', 'open', 'assigned', 'entered', 'external', 'internal', 'internally_published', 'pending', 'planned', 'private', 'prospective', 'Draft', 'published', 'testing', 'unassigned')")):
      ['path', 'portal_type', 'review_state', 'is_default_page', 'allowedRolesAndUsers'],
    ('allowedRolesAndUsers', 'path', 'sort_on', ('portal_type', "'Invoice'")):
      ['path', 'portal_type', 'allowedRolesAndUsers'],
    ('allowedRolesAndUsers', ('review_state', "['pending']")):
      ['review_state', 'allowedRolesAndUsers'],
    ('path',):
      ['path'],
  },
  '/intranet.psol/reference_catalog': {
    ('merge', 'sourceUID', ('relationship', "'relatesTo'")):
      ['sourceUID', 'relationship'],
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
    ('allowedRolesAndUsers', 'getResponsiblePerson', ('portal_type', "('ExtropyActivity', 'ExtropyFeature', 'ExtropyTask')"), ('review_state', "['open', 'in-progress', 'active', 'unassigned', 'deferred', 'assigned', 'testing', 'taskscomplete']")):
      ['getResponsiblePerson', 'review_state', 'portal_type', 'allowedRolesAndUsers'],
    ('allowedRolesAndUsers', 'path', ('meta_type', "'ExtropyActivity'")):
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
  },
  '/intranet.psol/extropy_timetracker_tool': {
    ('Creator', 'path', 'sort_on', 'start', ('allowedRolesAndUsers', "['Member', 'Manager', 'Authenticated', 'Finance-manager', 'user:AuthenticatedUsers', 'user:finance', 'Anonymous', 'user:geir']"), ('portal_type', "'ExtropyHours'")):
      ['path', 'start', 'Creator', 'allowedRolesAndUsers', 'portal_type'],
    ('Creator', 'path', 'sort_on', 'start', ('allowedRolesAndUsers', "['Member', 'Manager', 'Authenticated', 'Finance-manager', 'user:AuthenticatedUsers', 'user:finance', 'Anonymous', 'user:maria']"), ('portal_type', "'ExtropyHours'")):
      ['path', 'start', 'Creator', 'allowedRolesAndUsers', 'portal_type'],
    ('Creator', 'path', 'sort_on', 'start', ('allowedRolesAndUsers', "['Member', 'Manager', 'Authenticated', 'Finance-manager', 'user:AuthenticatedUsers', 'user:finance', 'Anonymous', 'user:martior']"), ('portal_type', "'ExtropyHours'")):
      ['path', 'start', 'Creator', 'allowedRolesAndUsers', 'portal_type'],
    ('Creator', 'path', 'sort_on', 'start', ('allowedRolesAndUsers', "['Member', 'Manager', 'Authenticated', 'user:AuthenticatedUsers', 'Anonymous', 'user:hannosch']"), ('portal_type', "'ExtropyHours'")):
      ['path', 'start', 'Creator', 'allowedRolesAndUsers', 'portal_type'],
    ('Creator', 'path', 'sort_on', 'start', ('allowedRolesAndUsers', "['Member', 'Manager', 'Authenticated', 'user:AuthenticatedUsers', 'Anonymous', 'user:lregebro']"), ('portal_type', "'ExtropyHours'")):
      ['path', 'start', 'Creator', 'allowedRolesAndUsers', 'portal_type'],
    ('Creator', 'path', 'sort_on', 'start', ('allowedRolesAndUsers', "['Member', 'Manager', 'Authenticated', 'user:AuthenticatedUsers', 'Anonymous', 'user:malthe']"), ('portal_type', "'ExtropyHours'")):
      ['path', 'start', 'Creator', 'allowedRolesAndUsers', 'portal_type'],
    ('Creator', 'path', 'sort_on', 'start', ('allowedRolesAndUsers', "['Member', 'Manager', 'Authenticated', 'user:AuthenticatedUsers', 'Anonymous', 'user:zeidler']"), ('portal_type', "'ExtropyHours'")):
      ['path', 'start', 'Creator', 'allowedRolesAndUsers', 'portal_type'],
    ('Creator', 'path', 'sort_on', 'start', ('allowedRolesAndUsers', "['Member', 'Manager', 'Authenticated', 'user:AuthenticatedUsers', 'user:contractors', 'Anonymous', 'user:denis']"), ('portal_type', "'ExtropyHours'")):
      ['path', 'start', 'Creator', 'allowedRolesAndUsers', 'portal_type'],
    ('Creator', 'sort_on', 'start', ('allowedRolesAndUsers', "['Member', 'Manager', 'Authenticated', 'Finance-manager', 'user:AuthenticatedUsers', 'user:finance', 'Anonymous', 'user:maria']"), ('portal_type', "'ExtropyHours'")):
      ['start', 'Creator', 'allowedRolesAndUsers', 'portal_type'],
    ('Creator', 'sort_on', 'start', ('allowedRolesAndUsers', "['Member', 'Manager', 'Authenticated', 'user:AuthenticatedUsers', 'Anonymous', 'user:lregebro']"), ('portal_type', "'ExtropyHours'")):
      ['start', 'Creator', 'allowedRolesAndUsers', 'portal_type'],
    ('UID', 'sort_on', ('allowedRolesAndUsers', "['Member', 'Manager', 'Authenticated', 'Finance-manager', 'user:AuthenticatedUsers', 'user:finance', 'Anonymous', 'user:maria']"), ('portal_type', "'ExtropyHours'")):
      ['UID', 'allowedRolesAndUsers', 'portal_type'],
    ('effectiveRange', 'path', 'sort_on', 'start', ('allowedRolesAndUsers', "['Anonymous', 'Anonymous', 'user:None']"), ('portal_type', "'ExtropyHours'")):
      ['path', 'allowedRolesAndUsers', 'start', 'portal_type'],
    ('path',):
      ['path'],
    ('path', 'sort_on', 'sort_order', 'start', ('allowedRolesAndUsers', "['Member', 'Manager', 'Authenticated', 'Finance-manager', 'user:AuthenticatedUsers', 'user:finance', 'Anonymous', 'user:martior']"), ('portal_type', "'ExtropyHours'")):
      ['path', 'start', 'allowedRolesAndUsers', 'portal_type'],
    ('path', 'sort_on', 'sort_order', 'start', ('allowedRolesAndUsers', "['Member', 'Manager', 'Authenticated', 'user:AuthenticatedUsers', 'Anonymous', 'user:hannosch']"), ('portal_type', "'ExtropyHours'")):
      ['path', 'start', 'allowedRolesAndUsers', 'portal_type'],
    ('path', 'sort_on', 'start', ('allowedRolesAndUsers', "['Member', 'Manager', 'Authenticated', 'Finance-manager', 'user:AuthenticatedUsers', 'user:finance', 'Anonymous', 'user:geir']"), ('portal_type', "'ExtropyHours'")):
      ['path', 'start', 'allowedRolesAndUsers', 'portal_type'],
    ('path', 'sort_on', 'start', ('allowedRolesAndUsers', "['Member', 'Manager', 'Authenticated', 'Finance-manager', 'user:AuthenticatedUsers', 'user:finance', 'Anonymous', 'user:maria']"), ('portal_type', "'ExtropyHours'")):
      ['path', 'start', 'allowedRolesAndUsers', 'portal_type'],
    ('path', 'sort_on', 'start', ('allowedRolesAndUsers', "['Member', 'Manager', 'Authenticated', 'Finance-manager', 'user:AuthenticatedUsers', 'user:finance', 'Anonymous', 'user:martior']"), ('portal_type', "'ExtropyHours'")):
      ['path', 'start', 'allowedRolesAndUsers', 'portal_type'],
    ('path', 'sort_on', 'start', ('allowedRolesAndUsers', "['Member', 'Manager', 'Authenticated', 'user:AuthenticatedUsers', 'Anonymous', 'user:hannosch']"), ('portal_type', "'ExtropyHours'")):
      ['path', 'start', 'allowedRolesAndUsers', 'portal_type'],
    ('path', 'sort_on', 'start', ('allowedRolesAndUsers', "['Member', 'Manager', 'Authenticated', 'user:AuthenticatedUsers', 'Anonymous', 'user:tomster']"), ('portal_type', "'ExtropyHours'")):
      ['path', 'start', 'allowedRolesAndUsers', 'portal_type'],
    ('path', 'sort_on', 'start', ('allowedRolesAndUsers', "['Member', 'Manager', 'Authenticated', 'user:AuthenticatedUsers', 'Anonymous', 'user:zeidler']"), ('portal_type', "'ExtropyHours'")):
      ['path', 'start', 'allowedRolesAndUsers', 'portal_type'],
    ('path', 'sort_on', 'start', ('allowedRolesAndUsers', "['Member', 'Manager', 'Authenticated', 'user:AuthenticatedUsers', 'user:contractors', 'Anonymous', 'user:denis']"), ('portal_type', "'ExtropyHours'")):
      ['path', 'start', 'allowedRolesAndUsers', 'portal_type'],
    ('path', 'sort_on', ('allowedRolesAndUsers', "['Member', 'Manager', 'Authenticated', 'Finance-manager', 'user:AuthenticatedUsers', 'user:finance', 'Anonymous', 'user:maria']"), ('portal_type', "'ExtropyHours'")):
      ['path', 'allowedRolesAndUsers', 'portal_type'],
    ('path', 'sort_on', ('allowedRolesAndUsers', "['Member', 'Manager', 'Authenticated', 'Finance-manager', 'user:AuthenticatedUsers', 'user:finance', 'Anonymous', 'user:martior']"), ('portal_type', "'ExtropyHours'")):
      ['path', 'allowedRolesAndUsers', 'portal_type'],
    ('path', 'sort_on', ('allowedRolesAndUsers', "['Member', 'Manager', 'Authenticated', 'user:AuthenticatedUsers', 'Anonymous', 'user:hannosch']"), ('portal_type', "'ExtropyHours'")):
      ['path', 'allowedRolesAndUsers', 'portal_type'],
    ('path', 'sort_on', ('allowedRolesAndUsers', "['Member', 'Manager', 'Authenticated', 'user:AuthenticatedUsers', 'Anonymous', 'user:lregebro']"), ('portal_type', "'ExtropyHours'")):
      ['path', 'allowedRolesAndUsers', 'portal_type'],
    ('path', 'sort_on', ('allowedRolesAndUsers', "['Member', 'Manager', 'Authenticated', 'user:AuthenticatedUsers', 'Anonymous', 'user:malthe']"), ('portal_type', "'ExtropyHours'")):
      ['path', 'allowedRolesAndUsers', 'portal_type'],
    ('path', 'sort_on', ('allowedRolesAndUsers', "['Member', 'Manager', 'Authenticated', 'user:AuthenticatedUsers', 'Anonymous', 'user:tomster']"), ('portal_type', "'ExtropyHours'")):
      ['path', 'allowedRolesAndUsers', 'portal_type'],
  },
}
