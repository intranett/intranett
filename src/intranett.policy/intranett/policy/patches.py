def allow_anonymous_robotstxt():
    from iw.rejectanonymous import addValidIds, addValidSubparts
    addValidIds('robots.txt')
    addValidIds('logged_out')
    addValidSubparts('portal_kss')


def apply():
    allow_anonymous_robotstxt()
