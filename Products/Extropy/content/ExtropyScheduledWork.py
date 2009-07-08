from AccessControl import ClassSecurityInfo
from Products.Archetypes.public import *
from Products.Extropy.config import *
from Products.Extropy.content.ExtropyBase import ExtropyBase, ExtropyBaseSchema, ParticipantsSchema, TimeSchema


ScheduledWorkSchema = ExtropyBaseSchema + TimeSchema + Schema((

    LinesField(
        name='participants',
        vocabulary='getAvailableParticipants',
        multiValued=1,
        widget=MultiSelectionWidget(
            label='Participants',
            description='',
            label_msgid='label_participants',
            description_msgid='help_participants',
            i18n_domain='extropy',
        ),
     ),
))

class ExtropyScheduledWork(ExtropyBase, BaseContent):
    """ExtropyScheduledWork content type.
    """

    schema = ScheduledWorkSchema
    meta_type = portal_type = archetype_name = 'ExtropyScheduledWork'
    archetype_name = 'Scheduled Work'
    content_icon = 'scheduledwork_icon.gif'
    security = ClassSecurityInfo()

    filter_content_types = 1
    allowed_content_types = []
    global_allow = 1


    def duration(self):
        """ the interval worked, in hours"""
        if not self.end() and self.start(): return 0

        if self.end() == self.end().latestTime() and self.start() == self.start().earliestTime():
            # a full workday is estimated to a set amount of hours.
        # we should have a global setting for what hours to expect from a WORKDAY
        # for now, we hardcode it to 6
            return 6

        interval = self.end() - self.start()
        iHours = round(interval * 24.0,1)
        if iHours < 0:
            return 0
        return iHours

registerType(ExtropyScheduledWork, PROJECTNAME)
