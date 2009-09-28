from Testing import ZopeTestCase

ZopeTestCase.installProduct('CMFCore', quiet=1)
ZopeTestCase.installProduct('CMFDefault', quiet=1)
ZopeTestCase.installProduct('CMFCalendar', quiet=1)
ZopeTestCase.installProduct('CMFTopic', quiet=1)
ZopeTestCase.installProduct('DCWorkflow', quiet=1)
ZopeTestCase.installProduct('CMFActionIcons', quiet=1)
ZopeTestCase.installProduct('CMFQuickInstallerTool', quiet=1)
ZopeTestCase.installProduct('CMFFormController', quiet=1)
ZopeTestCase.installProduct('GroupUserFolder', quiet=1)
ZopeTestCase.installProduct('ZCTextIndex', quiet=1)
ZopeTestCase.installProduct('TextIndexNG2', quiet=1)
ZopeTestCase.installProduct('SecureMailHost', quiet=1)
ZopeTestCase.installProduct('CSSRegistry', quiet=1)
ZopeTestCase.installProduct('CMFPlone')

ZopeTestCase.installProduct('Archetypes')
ZopeTestCase.installProduct('PortalTransforms', quiet=1)
ZopeTestCase.installProduct('MimetypesRegistry', quiet=1)
ZopeTestCase.installProduct('Extropy')
ZopeTestCase.installProduct('Invoice')
ZopeTestCase.installProduct('Memo')
ZopeTestCase.installProduct('TinyMCE')

from Products.PloneTestCase import PloneTestCase

PloneTestCase.setupPloneSite(extension_profiles=('Products.Extropy:extropy',))


class ExtropyTrackingTestCase(PloneTestCase.PloneTestCase):

    def _setup(self):
        PloneTestCase.PloneTestCase._setup(self)
