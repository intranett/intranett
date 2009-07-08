from plone.memoize import forever

# Remember the installed products and packages
from App import FactoryDispatcher

FactoryDispatcher._product_packages = \
    forever.memoize(FactoryDispatcher._product_packages)
