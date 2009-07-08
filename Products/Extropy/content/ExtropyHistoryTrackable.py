from AccessControl import ClassSecurityInfo
from Products.Archetypes.public import *
from Products.Extropy.config import *

from Products.CMFCore.utils import getToolByName
from AccessControl import getSecurityManager

from Products.CMFPlone.utils import _createObjectByType


class ExtropyHistoryTrackable:
    """Base class for Extropy objects that should make a history record on every change, typically tasks and bugs."""

    security = ClassSecurityInfo()

    def getChangenote(self):
        """Overrides the accessor, as changenote is a dummy field."""
        # don't remove
        return None

    def setChangenote(self, value):
        """Override the mutator, as changenote is a dummy field."""
        # don't remove
        return None

    def _rememberOriginalValues(self):
        originalvalues = []
        for field in self.Schema().editableFields(self):
            originalvalues.append({'title':field.widget.label,
                      'value':field.getEditAccessor(self)(),
                      'accessor':field.getEditAccessor(self),
                      'field':field.__name__
                      })
        return originalvalues

    def processForm(self, data=1, metadata=0, REQUEST=None, values=None):
        """Creates a TaskHistory on edit actions."""
        # First, remember the original values for comparisation
        originalvalues = self._rememberOriginalValues()

        changenote = ''

        # XXX: This part looks a bit messy, and should probably be cleaned up
        changenote = REQUEST is not None and REQUEST.get('changenote') or changenote
        changenote = self.REQUEST is not None and self.REQUEST.get('changenote') or changenote
        changenote = values is not None and values.get('changenote') or changenote

        # Do the field changes commitmment
        BaseFolder.processForm(self, data=1, metadata=0, REQUEST=REQUEST, values=values)
        changes = []

        # Run through the fields and make a record of changes
        for field in originalvalues:
            new =  field['accessor']()
            if new != field['value'] and field['field']not in  ['modification_date','text']:
                changes.append({'field': field['field'],
                                'title': field['title'],
                                'to'   : new,
                                'from' : field['value'] })

        # Only make objects if there is actually any data..
        if not changenote and not changes:
            return False
        newid = self.generateHistoryId()

        # Send mail
        self.extropy_notify_mail(client=self, REQUEST=REQUEST, changes=changes, changenote=changenote)

        # Create a history subobject with the changes
        _createObjectByType('ExtropyTaskHistory', self, newid)

        hist = getattr(self, newid)
        hist.setChangenote(changenote)
        hist.setChanges(changes)

    def getNosyPeopleEmails(self):
        """E-mails of nosy."""
        data = self.getNosyPeopleData()
        emails = [person['email'] for person in data]
        return emails

    def getNosyPeopleData(self):
        """Lookups data of involved people."""
        try:
            nosies = set(self.getNosy())
        except AttributeError:
            try:
                nosies = set(self.getParticipants())
            except AttributeError:
                nosies = set([])

        nosies.add(self.getExtropyProject().getProjectManager())
        if isinstance(self.getResponsiblePerson(), str):
            nosies.add(self.getResponsiblePerson())

        currentuser = getSecurityManager().getUser().getUserName()
        if currentuser in nosies:
            nosies.remove(currentuser)
        people = []
        membershiptool = getToolByName(self, 'portal_membership')
        for m in nosies:
            if m != currentuser:
                member = membershiptool.getMemberById(m)
                if member is not None:
                    mail = member.getProperty('email')
                    name = member.getProperty('fullname')
                    p = {'name': name, 'email': mail, 'userid': m}
                    people.append(p.copy())
        return people

    def SearchableText(self):
        """Also indexes the change notes."""
        orig = BaseFolder.SearchableText(self)
        changes = [i.getChangenote() for i in self.getHistory()]
        return ' '.join(changes) + orig

    def getHistory(self):
        """Gets all changenotes for this object."""
        changes = list(self.objectValues('ExtropyTaskHistory'))
        changes.reverse()
        return changes

    security.declareProtected('View','HistoryId')
    def generateHistoryId(self):
        """Overrides the unique-id generator to get sequential numbering."""
        if not hasattr(self,'history_id_counter'):
            self.history_id_counter = 1
        newid = self.history_id_counter
        self.history_id_counter = newid + 1
        return 'change-' + str(newid)
