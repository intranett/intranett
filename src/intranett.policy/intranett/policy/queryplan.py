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
}
