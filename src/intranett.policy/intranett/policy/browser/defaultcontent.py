# -*- coding: utf-8 -*-

from zope.publisher.browser import BrowserView


class DefaultContent(BrowserView):

    def __call__(self):
        wf = self.context.portal_workflow

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
            '(Dette innholdet er hentet fra hjelp.intranett.no og kan slettes når det ikke er behov for lengre)',
            text=GRUNNLEGGENDE_BRUK,
            text_format='html')
        grunnleggende_bruk = kom_i_gang['grunnleggende-bruk']
        grunnleggende_bruk.processForm()
        wf.doActionFor(grunnleggende_bruk, 'publish')
        grunnleggende_bruk.reindexObject()

        # Aktuelt folder
        self.context.invokeFactory('Folder',
            id='nyheter',
            title='Nyheter',
            description='Nyheter og oppdateringer på intranettet.')
        nyheter = self.context['nyheter']
        nyheter.processForm()
        wf.doActionFor(nyheter, 'publish')
        nyheter.reindexObject()

        # Initial news item
        nyheter.invokeFactory('News Item',
            id='nytt-intranett',
            title='Nytt intranett',
            description='Det nye intranettet er klart til bruk.',
            text=NYTT_INTRANETT,
            text_format='html')
        nytt_intranett = nyheter['nytt-intranett']
        nytt_intranett.processForm()
        wf.doActionFor(nytt_intranett, 'publish')
        nytt_intranett.reindexObject()

        # Go to frontpage
        self.request.response.redirect(self.context.portal_url())
        return 'done'


NYTT_INTRANETT="""\
<p>Intranettet lar oss dele dokumenter, tekst, bilder, nyheter og interninformasjon på en lettvint måte.</p>
<p>Du kan nå intranettet overalt hvor du har internett-tilgang.</p>
"""

GRUNNLEGGENDE_BRUK = """\
<p>Intranettet har "innhold" av forskjellige typer, for eksempel nyhetsartikler, bilder, filer og sider. Det er personen som legger til innholdet som bestemmer hva slags type det er.</p>
<p>Når noen har lagt til innhold, og publisert det, vil det være synlig for de andre brukerne av intranettet. Det vil dukke opp i menyene og i relevante søkeresultater.</p>
<p><span style="padding-left: 0px; ">Innholdet er ordnet i mapper, akkurat som man gjør på sin egen datamaskin. Det er mappene som bestemmer hva menystrukturen blir.</span></p>
<h3>Brukerkonto</h3>
<p>For å kunne se intranettet må du ha en brukerkonto. Brukerkontoen er personlig og har et eget brukernavn og et passord bare for deg.</p>
<p>Du må bruke brukernavnet og passordet sammen for å kunne logge inn på intranettet. Det er viktig at du ikke deler brukerkontoen din og passordet ditt med andre.</p>
<p>Personer uten brukerkonto har ikke tilgang til intranettet.</p>
<h3>Tilgangskontroll</h3>
<p>Forskjellige brukerkontoer kan ha forskjellige tilgangsrettigheter i forskjellige mapper. Om du ikke har tilgang til å se en mappe, vil den ikke være synlig for deg.</p>
<p>Noen brukere har lov å legge til eller redigere innhold. Administratorbrukere kan legge til eller endre innhold overalt i intranettet, mens andre brukere gjerne får tildelt muligheten til å legge til innhold i en egen mappe eller en mappe for sin avdeling.</p>
"""

