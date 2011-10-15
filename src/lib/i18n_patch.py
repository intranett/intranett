from zope.tal import talinterpreter


def _unicode_replace(structure):
    if isinstance(structure, str):
        text = structure.decode('utf-8', 'replace')
    else:
        text = unicode(structure)
    return text


def getvalue(self):
    try:
        return u''.join(self)
    except UnicodeDecodeError:
        return u''.join([_unicode_replace(value) for value in self])


def apply():
    talinterpreter.FasterStringIO.getvalue = getvalue
