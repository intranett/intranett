from StringIO import StringIO

from collective.ATClamAV.testing import EICAR
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
import transaction

from intranett.policy.tests.base import get_browser
from intranett.policy.tests.base import IntranettFunctionalTestCase


class TestClamAVValidator(IntranettFunctionalTestCase):

    level = 2

    def test_atvirusfile(self):
        # Setup
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ['Manager'])
        portal.invokeFactory('Folder', 'virus-folder')
        setRoles(portal, TEST_USER_ID, ['Member'])
        transaction.commit()

        # Test if a virus-infected file gets caught by the validator
        browser = get_browser(self.layer['app'])
        browser.open(portal.absolute_url() + '/virus-folder')
        browser.getLink(url='createObject?type_name=File').click()
        control = browser.getControl(name='file_file')
        control.filename = 'virus.txt'
        control.value = StringIO(EICAR)
        browser.getControl(name='form.button.save').click()
        self.assertTrue('Validation failed, file is virus-infected.' in
            browser.contents)

        # And let's see if a clean file passes...
        browser.open(portal.absolute_url() + '/virus-folder')
        browser.getLink(url='createObject?type_name=File').click()
        control = browser.getControl(name='file_file')
        control.filename = 'nonvirus.txt'
        control.value = StringIO('Not a virus')
        browser.getControl(name='form.button.save').click()
        self.assertFalse('Validation failed, file is virus-infected.' in
            browser.contents)
        self.assertTrue(browser.url.endswith('/view'))
        self.assertTrue('Not a virus' in browser.contents)
