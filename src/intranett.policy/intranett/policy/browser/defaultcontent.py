# -*- coding: utf-8 -*-

from zope.publisher.browser import BrowserView


class DefaultContent(BrowserView):

    def __call__(self):
        wf = self.context.portal_workflow

        # Aktuelt folder
        self.context.invokeFactory('Folder',
            id='aktuelt',
            title='Aktuelt og nytt',
            description='Nyheter og oppdateringer på intranettet.')
        aktuelt = self.context['aktuelt']
        aktuelt.processForm()
        wf.doActionFor(aktuelt, 'publish')
        aktuelt.reindexObject()

        # Initial news item
        aktuelt.invokeFactory('News Item',
            id='nytt-intranett',
            title='Nytt intranett',
            description='Det nye intranettet er klart til bruk.',
            text='<p>Intranettet lar oss dele dokumenter, tekst, bilder, '
            'nyheter og interninformasjon på en lettvint måte.</p>\n'
            '<p>Du kan nå intranettet overalt hvor du har internett-tilgang.</p>',
            text_format='html')
        nytt_intranett = aktuelt['nytt-intranett']
        nytt_intranett.processForm()
        wf.doActionFor(nytt_intranett, 'publish')
        nytt_intranett.reindexObject()

        # Kom i gang folder
        self.context.invokeFactory('Folder',
            id='kom-i-gang',
            title='Kom i gang',
            description='Hvordan komme raskt i gang.')
        kom_i_gang = self.context['kom-i-gang']
        kom_i_gang.processForm()
        wf.doActionFor(kom_i_gang, 'publish')
        kom_i_gang.reindexObject()

        # Grunnleggende bruk page
        kom_i_gang.invokeFactory('Document',
            id='grunnleggende-bruk',
            title='Grunnleggende bruk',
            description='Kom i gang med bruk av intranettet. '
            '(Dette innholdet er hentet fra hjelp.intranett.no og kan slettes når det ikke er behov for lengre)')

        self.request.response.redirect(self.context.portal_url())
        return 'done'

