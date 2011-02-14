from pkg_resources import get_distribution
from Products.GenericSetup.interfaces import EXTENSION
from Products.GenericSetup.registry import _import_step_registry
from Products.GenericSetup.registry import _profile_registry
from Products.GenericSetup.upgrade import _registerUpgradeStep
from Products.GenericSetup.upgrade import UpgradeStep
from Products.GenericSetup.zcml import _import_step_regs
import venusian
from zope.dottedname.resolve import resolve


class Configurator(object):

    def __init__(self, package):
        self.package_name, self.package = self.maybe_dotted(package)
        self.package_version = get_distribution(self.package_name).version
        self.policy_profile = u'%s:default' % self.package_name
        self.upgrades = []

    def scan(self, package=None, categories=('plutonian', )):
        if package is None:
            package = self.package
        scanner = venusian.Scanner(config=self)
        scanner.scan(package, categories=categories)

    def maybe_dotted(self, package):
        if isinstance(package, basestring):
            name = package
            package = resolve(name)
        else:
            name = package.__name__
        return (name, package)

    def add_import_step(self, name, handler, depends):
        _import_step_regs.append(name)
        _import_step_registry.registerStep(name, handler=handler,
            dependencies=depends, title=name)

    def add_upgrade_step(self, name, handler, destination):
        step = UpgradeStep(u'Upgrade %s' % name, self.policy_profile,
            str(destination - 1), str(destination), None, handler,
            checker=None, sortkey=0)
        if destination in self.upgrades:
            raise ValueError('Duplicate upgrade step to destination %s'
                % destination)
        self.upgrades.append(destination)
        _registerUpgradeStep(step)

    def last_upgrade_to(self):
        return unicode(max(self.upgrades))

    def register_profile(self, package_name=None):
        if package_name is None:
            package_name = self.package_name
        title = '%s:default' % package_name
        _profile_registry.registerProfile('default', title, description=u'',
            path='profiles/default', product=package_name,
            profile_type=EXTENSION)


class import_step(object):

    def __init__(self, depends=('toolset', 'types', 'workflow')):
        self.depends = depends

    def register(self, scanner, name, wrapped):
        config = scanner.config
        name = wrapped.__module__ + name
        config.add_import_step(name, wrapped, self.depends)

    def __call__(self, wrapped):
        venusian.attach(wrapped, self.register, category='plutonian')
        return wrapped


class upgrade_to(object):

    def __init__(self, destination):
        self.destination = destination

    def register(self, scanner, name, wrapped):
        config = scanner.config
        config.add_upgrade_step(name, wrapped, self.destination)

    def __call__(self, wrapped):
        venusian.attach(wrapped, self.register, category='plutonian')
        return wrapped
