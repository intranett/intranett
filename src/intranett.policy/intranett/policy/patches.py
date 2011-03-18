def allow_anonymous_robotstxt():
    from iw.rejectanonymous import addValidIds, addValidSubparts
    addValidIds('robots.txt')
    addValidIds('logged_out')
    addValidSubparts('portal_kss')


def add_mime_types():
    import os
    from zope.contenttype import add_files
    here = os.path.dirname(os.path.abspath(__file__))
    add_files([os.path.join(here, "mime.types")])


def apply():
    allow_anonymous_robotstxt()
    add_mime_types()
