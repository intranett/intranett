from Products.CMFCore.permissions import setDefaultRoles

PROJECTNAME = 'jarn.extranet'

GLOBALS = globals()


ADD_PERMISSIONS = {
    'Customer': 'jarn.extranet: Add Customer',
    'Person': 'jarn.extranet: Add Person',
    'Contract': 'jarn.extranet: Add Contract',
    'SiteDocumentation': 'jarn.extranet: Add SiteDocumentation',


}

for p in ADD_PERMISSIONS.values():
    setDefaultRoles(p, ('Owner','Manager'))
