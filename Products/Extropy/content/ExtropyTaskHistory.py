from AccessControl import ClassSecurityInfo
from Products.Archetypes.public import *
from Products.Extropy.config import *
from Products.CMFCore.utils import getToolByName
from Acquisition import aq_base, aq_parent

TaskHistorySchema = BaseSchema.copy() +  Schema((
          TextField('changenote',
              default_output_type='text/x-html-safe',
              default_content_type='text/plain',
              allowable_content_types=('text/plain'),
              widget=TextAreaWidget(label='Changenote',
                                    description='',
                                    label_msgid='',
                                    description_msgid='',
                                    i18n_domain='extropy',
                                    rows=5),
              ),
          ))

class ExtropyTaskHistory(BaseContent):
    """A comment, change or similar to the containing task."""

    schema = TaskHistorySchema
    security = ClassSecurityInfo()

    def Title(self):
        """ title override"""
        return self.getRawChangenote()[:30] or self.getId()

    def setChanges(self,changes):
        """ save a list of changed attributes in the parent object"""
        # for example ({'title':attribute, 'from':old, 'to':new},)
        self.changes = tuple(changes)

    def getChanges(self):
        """ retrieve the saved changes"""
        if hasattr(self, 'changes') and self.changes:
            return self.changes
        return None

    # security.declareProtected(MODIFY_CONTENT_PERMISSION , 'indexObject')
    # def indexObject(self):
    #     """"""
    #     #parent will reindex itself when we are added
    #     pass
    #     #self.aq_parent.reindexObject()
    # 
    # security.declareProtected(MODIFY_CONTENT_PERMISSION , 'unindexObject')
    # def unindexObject(self):
    #     """"""
    #     # reindex parent if we are removed
    #     self.aq_parent.reindexObject()
    # 
    # security.declareProtected(MODIFY_CONTENT_PERMISSION , 'reindexObject')
    # def reindexObject(self, idxs=[]):
    #     """"""
    #     # reindex parent if we are changed
    #     self.aq_parent.reindexObject(idxs)


registerType(ExtropyTaskHistory, PROJECTNAME)
