def allow_anonymous_robotstxt():
    from iw.rejectanonymous import addValidIds
    addValidIds('robots.txt')

def apply():
    allow_anonymous_robotstxt()
