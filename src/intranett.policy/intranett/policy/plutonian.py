from Products.GenericSetup.registry import _import_step_registry
from Products.GenericSetup.zcml import _import_step_regs
import venusian
from zope.dottedname.resolve import resolve


class Configurator(object):

    def scan(self, package, categories=('plutonian', )):
        package = self.maybe_dotted(package)
        scanner = venusian.Scanner(config=self)
        scanner.scan(package, categories=categories)

    def maybe_dotted(self, package):
        if isinstance(package, basestring):
            package = resolve(package)
        return package

    def add_import_step(self, name, handler, depends):
        _import_step_regs.append(name)
        _import_step_registry.registerStep(name, handler=handler,
            dependencies=depends, title=name)


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
