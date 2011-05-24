from re import search
from Record import Record

def safe_unicode(v):
    if isinstance(v, unicode):
        return v
    return unicode(v, 'utf-8', 'replace')


def dictifyBrain(item):
    """Make a dict with all the metadata
    and getURL and getPath"""
    d = {}
    if isinstance(item, Record):
        for key in item.__record_schema__.keys():
            d[key] = getattr(item, key)
        d['getPath'] = item.getPath()
        d['getURL'] = item.getURL()
        if d.has_key('UID'):
            d['uid'] = d['UID']
    return d

def activity(data):
    # Group by task/activity typically indicated by #455 or keywords like
    # meeting, discussion, mgmt/management, test, release in Title
    nodekey = data
    nodekey = getattr(nodekey, 'Title')
    if callable(nodekey):
        nodekey = nodekey()
    m = search('(^#?|#)(\d+)', nodekey)
    if m:
        return m.group(2)
    elif search('[Rr]eleas(ing|e)', nodekey):
        return 'Release'
    elif search('[Pp]lan(ing|ed|\s)|[Mm]eeting|[Dd]iscuss(ion|ed|\s)', nodekey):
        return 'Communication'
    elif search('[Mm](anage(ment|d|\s)|gmt)', nodekey):
        return 'Project mgmt'
    elif search('[Tt]est(ing|ed|\s)', nodekey):
        return 'Testing'
    else:
        return 'Other'
