from zope.publisher.browser import BrowserView


class FrontpageView(BrowserView):
    """Frontpage view
    """
    
    def columns_class(self):
        ploneview = self.context.restrictedTraverse('@@plone')
        cols = ['frontpage.portlets.left',
                'frontpage.portlets.central',
                'frontpage.portlets.right']
        i = 0
        for manager in cols:
            if ploneview.have_portlets(manager, self):
                i+=1
        return 'width-%s' % (16/i)
