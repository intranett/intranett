from Products.Five.browser import BrowserView

from xml.sax.saxutils import escape

class ProgressBar(BrowserView):
    _html = '''\
        <a class="progressbar" href="%(URL)s/timereport2"%(extra)s>
            %(bar)s
        </a>
        <p class="discreet" style="clear:left;">
            %(worked)s hours worked, %(remaining)s hours remain
        </p><div style="clear:both">&nbsp;</div>'''

    _worked = '<span class="progressbar-done"></span>'
    _worked_short = '<span class="progressbar-done short"></span>'
    _remaining = '<span class="progressbar-remaining"></span>'
    _remaining_short = '<span class="progressbar-remaining short"></span>'
    _no_estimate = '<span class="progressbar-remaining">&raquo;</span>'
    _elipsis = '<span class="progressbar-elipsis">&hellip;</span>'
    _elipsis_size = 30

    def __call__(self, worked=0, remaining=0, URL=None, **kw):
        worksize = int(worked)
        remainsize = int(remaining)
        large = (worksize + remainsize) > self._elipsis_size
        if large:
            worksize = min(worksize, self._elipsis_size)
            remainsize = min(remainsize, self._elipsis_size - worksize)

        bar = self._worked * worksize + self._remaining * remainsize
        bar += large and self._elipsis or ''
        if not bar:
            if worked or remaining:
                # Timespans shorter than 1 hour
                bar = (worked > remaining and self._worked_short or
                                              self._remaining_short)
            else:
                bar = self._no_estimate

        extra = ' '.join('%s="%s"' % (k, escape(v)) for (k, v) in kw.iteritems())
        extra = extra and ' ' + extra

        return self._html % locals()

class SmallProgressBar(ProgressBar):
    _html = '''\
        <a class="progressbar-small" href="%(URL)s/timereport2"
           title="%(worked)s hours worked, %(remaining)s hours remain"%(extra)s>
            %(bar)s
        </a>'''
