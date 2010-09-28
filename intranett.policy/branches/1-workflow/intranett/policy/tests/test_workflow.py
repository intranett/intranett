import doctest

from Products.CMFCore.utils import getToolByName
from Testing.ZopeTestCase import FunctionalDocFileSuite as Suite

from intranett.policy.tests.base import IntranettTestCase
from intranett.policy.tests.base import IntranettFunctionalTestCase

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
            'ATSortCriterion', 'Discussion Item', 'FieldsetFolder',
            'FormBooleanField', 'FormCaptchaField', 'FormCustomScriptAdapter',
            'FormDateField', 'FormFileField', 'FormFixedPointField',
            'FormIntegerField', 'FormLabelField', 'FormLikertField',
            'FormLinesField', 'FormMailerAdapter', 'FormMultiSelectionField',
            'FormPasswordField', 'FormRichLabelField', 'FormRichTextField',
            'FormSaveDataAdapter', 'FormSelectionField', 'FormStringField',
            'FormTextField', 'FormThanksPage', 'Plone Site', 'TempFolder',
        ])
        asset_workflow = set([
            'File', 'Image',
        ])
        types = set(ttool.keys()) - no_workflow - asset_workflow
        for type_ in types:
            wf = self.wftool.getChainForPortalType(type_)
            self.assertEquals(wf, ('intranett_workflow', ),
                              'Found workflow %s for type %s, expected '
                              '(\'intranett_workflow\'), ' % (wf, type_))


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestWorkflowSetup))
    suite.addTest(Suite('workflow.txt',
                        optionflags=OPTIONFLAGS,
                        test_class=IntranettFunctionalTestCase))
    return suite
