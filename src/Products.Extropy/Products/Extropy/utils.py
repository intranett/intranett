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