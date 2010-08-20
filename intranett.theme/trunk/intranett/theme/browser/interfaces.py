from plone.theme.interfaces import IDefaultPloneLayer
from zope.viewlet.interfaces import IViewletManager

class IThemeSpecific(IDefaultPloneLayer):
    """Marker interface that defines a Zope browser layer.
    """
    
class IAboveColumns(IViewletManager):
    """A viewlet manager that sits above the columns
    """    
