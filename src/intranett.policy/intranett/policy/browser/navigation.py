from Products.CMFPlone.browser import navigation


class CatalogNavigationTabs(navigation.CatalogNavigationTabs):

    def topLevelTabs(self, actions=None, category='portal_tabs'):
        # We override tabs generator to have the users listing show up last
        original = super(CatalogNavigationTabs, self).topLevelTabs(
            actions=actions, category=category)

        result = []
        users_info = None
        for info in original:
            if info['id'] == 'users':
                users_info = info
            else:
                result.append(info)

        if users_info is not None:
            result.append(users_info)

        return result
