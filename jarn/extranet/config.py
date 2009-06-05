from Products.CMFCore.permissions import setDefaultRoles

PROJECTNAME = 'jarn.extranet.customer'

GLOBALS = globals()


ADD_PERMISSIONS = {
    'Customer': 'jarn.extranet.customer: Add Customer',
    'Person': 'jarn.extranet.customer: Add Person',
}

for p in ADD_PERMISSIONS.values():
    setDefaultRoles(p, ('Owner','Manager'))
