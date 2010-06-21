# query plan dumped at 'Mon Jun 21 20:53:01 2010'

queryplan = {
  '/Plone/portal_catalog': {
    ('path',):
      ['path'],
    ('path', 'show_inactive', 'sort_on', ('allowedRolesAndUsers', "['Manager', 'Authenticated', 'Anonymous', 'user:admin']")):
      ['path', 'allowedRolesAndUsers'],
    ('path', 'sort_on', 'sort_order', ('allowedRolesAndUsers', "['Manager', 'Authenticated', 'Anonymous', 'user:admin']"), ('is_default_page', 'False'), ('portal_type', "['Document', 'Event', 'File', 'Folder', 'FormFolder', 'Image', 'Large Plone Folder', 'Link', 'News Item', 'Topic']")):
      ['path', 'allowedRolesAndUsers', 'is_default_page', 'portal_type'],
    ('path', 'sort_on', 'sort_order', ('allowedRolesAndUsers', "['Manager', 'Authenticated', 'Anonymous', 'user:admin']"), ('is_default_page', 'False'), ('portal_type', "['Document', 'Folder']")):
      ['path', 'allowedRolesAndUsers', 'is_default_page', 'portal_type'],
  },
  '/Plone/portal_catalog:valueindexes': frozenset([
    'Creator',
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
