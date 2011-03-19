PROJECTNAME = 'intranett.policy'
ADD_PERMISSIONS = {'MembersFolder': '%s: Add MembersFolder' % PROJECTNAME}
MEMBERS_FOLDER_ID = 'users'

from plutonian import Configurator

config = Configurator('intranett.policy')
