from Products.Five.browser import BrowserView

from xml.sax.saxutils import escape

class ProgressBar(BrowserView):
    _html = '''\
        <a class="progressbar" href="%(URL)s/timereport2"%(extra)s>
            %(bar)s
        </a>
        <p class="discreet" style="clear:left;">
            %(worked)s hours worked
        </p><div style="clear:both">&nbsp;</div>'''

    _worked = '<span class="progressbar-done"></span>'
    _worked_short = '<span class="progressbar-done short"></span>'
    _no_estimate = '<span class="progressbar-remaining">&raquo;</span>'
    _elipsis = '<span class="progressbar-elipsis">&hellip;</span>'
    _elipsis_size = 30

    def __call__(self, worked=0, URL=None, **kw):
        worksize = int(worked)
        large = worksize > self._elipsis_size
        if large:
            worksize = min(worksize, self._elipsis_size)

        bar = self._worked * worksize
        bar += large and self._elipsis or ''
        if not bar:
            if worked:
                bar = self._worked_short
            else:
                bar = self._no_estimate

        extra = ' '.join('%s="%s"' % (k, escape(v)) for (k, v) in kw.iteritems())
        extra = extra and ' ' + extra

        return self._html % locals()

class SmallProgressBar(ProgressBar):
    _html = '''\
        <a class="progressbar-small" href="%(URL)s/timereport2"
           title="%(worked)s hours worked"%(extra)s>
            %(bar)s
        </a>'''
