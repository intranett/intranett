from Testing import ZopeTestCase
from Products.Invoice.tests import InvoiceTestCase


class TestInvoice(InvoiceTestCase.InvoiceTestCase):

    def afterSetUp(self):
        self.folder.invokeFactory('Invoice','testinvoice')
        self.invoice = self.folder.testinvoice

    def testAddingInvoiceLines(self):
        vals = [{'item':'1', 'description':'FOO BAR', 'amount':'123'}]
        self.invoice.setInvoiceLines(vals)
        self.assertEqual(self.invoice.getInvoiceLines()[0]['amount'], '123')

    def testCalculatingTotals(self):
        vals = [
                {'item':'1', 'description':'FOO', 'amount':'2.000'},
                {'item':'2', 'description':'BAR', 'amount':'2'}
                ]
        self.invoice.setInvoiceLines(vals)
        self.assertEqual(self.invoice.calculatetotal(), 4.00)

    def testCalculatingTotalsWithBogusValues(self):
        vals = [
                {'item':'1', 'description':'eggs', 'amount':'2.4'},
                {'item':'2', 'description':'ham', 'amount':'FISH'},
                {'item':'3', 'description':'spam', 'amount':''}

                ]
        self.invoice.setInvoiceLines(vals)
        self.assertEqual(self.invoice.calculatetotal(), '*ERROR*')

    def testCalculatingDueDate(self):
        self.invoice.setInvoiceDate('2006/01/01')
        self.invoice.setPaymentDays(1)
        self.assertEqual(self.invoice.getPaymentdue().Date(), '2006/01/02')

    def testCalculatingTitle(self):
        self.invoice.setInvoiceNumber(123)
        self.assertEqual(self.invoice.Title(), '#123')
        
    def testInvoiceNumber(self):
        self.assertEqual(self.invoice.getInvoiceNumber(), 1)
        
    def testDefaultInvoiceNumber(self):
        self.invoice.setInvoiceNumber(123)
        self.invoice.reindexObject()
        self.folder.invokeFactory('Invoice','newinvoice')
        self.assertEqual(self.folder.newinvoice.getDefaultInvoiceNumber(),
                         self.invoice.getInvoiceNumber() + 1)

    def testDefaultInvoiceNumberReturnsHighestPlusOne(self):
        self.folder.invokeFactory('Invoice','testinvoice42', invoiceNumber=42)
        self.folder.invokeFactory('Invoice','testinvoice111', invoiceNumber=111)
        self.folder.invokeFactory('Invoice','testinvoice1', invoiceNumber=1)
        self.folder.invokeFactory('Invoice','newinvoice')
        self.assertEqual(self.folder.newinvoice.getDefaultInvoiceNumber(), 112)

    def testgenerateNewId(self):
        self.invoice.setInvoiceNumber(22)
        self.assertEqual(self.invoice.generateNewId(),'invoice-00022')

    def testWorkflowInstalled(self):
        self.failUnless('invoice_workflow' in self.portal.portal_workflow.objectIds())

    def testWorkflowAssignedToInvoice(self):
        wf_tool = self.portal.portal_workflow
        self.failUnlessEqual(wf_tool.getChainForPortalType('Invoice'), ('invoice_workflow',))

    def testInitialState(self):
        wf_tool = self.portal.portal_workflow
        self.assertEqual(wf_tool.getInfoFor(self.folder.testinvoice, 'review_state'), 'Draft')

    def testSendingInvoice(self):
        wf_tool = self.portal.portal_workflow
        wf_tool.doActionFor(self.folder.testinvoice, 'send')
        self.assertEqual(wf_tool.getInfoFor(self.folder.testinvoice, 'review_state'), 'Sent')

    def testRecurInvoice(self):
        l = len(self.folder.objectIds())
        self.invoice.createRecurrence()
        self.assertEqual(len(self.folder.objectIds()), l+1)
        
def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestInvoice))
    return suite
