
class LocalRoles(object):
    """Provide a local role manager for customers
    """
    def __init__(self, context):
        self.context = context

    #
    #   ILocalRoleProvider implementation
    #
    def getAllRoles(self):
        # We don't use generator with memoize
        return [(o.getUserName(),('Reader','Member')) for o in self.context.listFolderContents(contentFilter={"portal_type" : "Person"})]

    def getRoles(self, principal_id):
        # We don't use generator with memoize
        result = {}
        for (pid,roles) in self.getAllRoles():
            if pid == principal_id:
                result.update(dict.fromkeys(roles))
        return tuple(result.keys())
