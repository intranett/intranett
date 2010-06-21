from time import time

from Products.PloneTestCase import ptc
from Products.PloneTestCase.setup import cleanupPloneSite
from Products.PloneTestCase.setup import SiteSetup

from intranett.policy.tests import layer


def setupSite(id=ptc.portal_name,
              policy=ptc.default_policy,
              products=ptc.default_products,
              quiet=True,
              with_default_memberarea=True,
              base_profile=ptc.default_base_profile,
              extension_profiles=(),
              default_extension_profiles=ptc.default_extension_profiles):
    cleanupPloneSite(id)
    if default_extension_profiles:
        extension_profiles = list(default_extension_profiles) + \
            list(extension_profiles)
    IntranettSiteSetup(id, policy, products, quiet, with_default_memberarea,
                       base_profile, extension_profiles).run()


class IntranettSiteSetup(SiteSetup):

    def _setupPloneSite_with_genericsetup(self):
        start = time()
        if self.base_profile != ptc.default_base_profile:
            self._print('Adding Plone Site (%s) ... ' % (self.base_profile,))
        else:
            self._print('Adding Plone Site ... ')
        # Add Plone site
        from Products.CMFPlone.factory import addPloneSite
        addPloneSite(self.app, self.id, profile_id=self.base_profile,
                     setup_content=False)
        self._commit()
        self._print('done (%.3fs)\n' % (time()-start,))


ptc.installProduct("PloneFormGen", quiet=1)
setupSite()


class IntranettTestCase(ptc.PloneTestCase):
    """ base class for integration tests """

    layer = layer.intranett


class IntranettFunctionalTestCase(ptc.FunctionalTestCase):
    """ base class for functional tests """

    layer = layer.intranett
