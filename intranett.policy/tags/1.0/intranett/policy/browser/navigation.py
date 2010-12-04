from Products.CMFPlone.browser import navigation


class CatalogNavigationTabs(navigation.CatalogNavigationTabs):

    def topLevelTabs(self, actions=None, category='portal_tabs'):
        # We override tabs generator to have the employee listing show up last
        original = super(CatalogNavigationTabs, self).topLevelTabs(
            actions=actions, category=category)

        result = []
        employee_info = None
        for info in original:
            if info['id'] == 'employee-listing':
                employee_info = info
            else:
                result.append(info)

        if employee_info is not None:
            result.append(employee_info)

        return result
