import doctest

from AccessControl import getSecurityManager
from Products.CMFCore.utils import getToolByName

from intranett.policy.tests.base import IntranettTestCase

OPTIONFLAGS = (doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE)


class TestWorkflowSetup(IntranettTestCase):

    def afterSetUp(self):
        self.wftool = getToolByName(self.portal, 'portal_workflow')

    def test_workflow_assignments(self):
        ttool = getToolByName(self.portal, 'portal_types')
        no_workflow = set([
            'ATBooleanCriterion', 'ATCurrentAuthorCriterion',
            'ATDateCriteria', 'ATDateRangeCriterion', 'ATListCriterion',
            'ATPathCriterion', 'ATPortalTypeCriterion', 'ATReferenceCriterion',
            'ATRelativePathCriterion', 'ATSelectionCriterion',
            'ATSimpleIntCriterion', 'ATSimpleStringCriterion',
            'ATSortCriterion', 'FieldsetFolder', 'FormBooleanField',
            'FormCaptchaField', 'FormCustomScriptAdapter', 'FormDateField',
            'FormFileField', 'FormFixedPointField', 'FormIntegerField',
            'FormLabelField', 'FormLikertField', 'FormLinesField',
            'FormMailerAdapter', 'FormMultiSelectionField',
            'FormPasswordField', 'FormRichLabelField', 'FormRichTextField',
            'FormSaveDataAdapter', 'FormSelectionField', 'FormStringField',
            'FormTextField', 'FormThanksPage', 'Plone Site',
        ])
        for type_ in no_workflow:
            wf = self.wftool.getChainForPortalType(type_)
            self.assertEquals(wf, (),
                              'Found workflow %s for type %s, expected '
                              '(), ' % (wf, type_))

        workflows = {
            'Discussion Item': ('one_state_workflow', ),
            'File': (),
            'Image': (),
        }
        for type_ in set(ttool.keys()) - no_workflow:
            wf = self.wftool.getChainForPortalType(type_)
            expected = workflows.get(type_, ('intranett_workflow', ))
            self.assertEquals(wf, expected,
                              'Found workflow %s for type %s, expected '
                              '%s, ' % (wf, type_, expected))

    def test_no_anonymous_view(self):
        self.logout()
        sm = getSecurityManager()
        self.assertFalse(sm.checkPermission('View', self.folder))
        # We don't want this, but we first need to make sure the login form
        # and standard error message views work without anon View permission
        # on the portal object
        self.assertTrue(sm.checkPermission('View', self.portal))

        front = self.portal['front-page']
        self.assertEquals(front.workflow_history.keys()[-1],
                          'intranett_workflow')
        self.assertFalse(sm.checkPermission('View', front))


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestWorkflowSetup))
    return suite
