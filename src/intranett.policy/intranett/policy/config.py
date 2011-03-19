PROJECTNAME = 'intranett.policy'
ADD_PERMISSIONS = {'MembersFolder': 'intranett.policy: Add MembersFolder'}
MEMBERS_FOLDER_ID = 'people'
MEMBERS_FOLDER_TITLE = 'Personer' # 'People'

from plutonian import Configurator

config = Configurator('intranett.policy')
