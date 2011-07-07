def allow_anonymous_robotstxt():
    from iw.rejectanonymous import addValidIds, addValidSubparts
    addValidIds('robots.txt')
    addValidIds('logged_out')
    addValidSubparts('portal_kss')


def allow_anonymous_activation():
    from iw.rejectanonymous import addValidIds, addValidSubparts
    addValidIds('activate_form')
    addValidSubparts('activate')


def apply():
    allow_anonymous_robotstxt()
    allow_anonymous_activation()
