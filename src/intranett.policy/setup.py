import os
import os.path

from setuptools import setup, find_packages

changes = os.path.join(os.pardir, os.pardir, 'CHANGES.txt')
lines = []
with open(changes, 'rU') as fd:
    for line in fd:
        if line.startswith('---'):
            break
        lines.append(line)

version = lines[-1].split('-')[0].strip()
if 'unreleased' in lines[-1]:
    version += 'dev'

setup(name='intranett.policy',
      version=version,
      description="",
      long_description=open("README.txt").read(),
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='',
      author='Jarn AS',
      author_email='info@jarn.com',
      url="",
      license='GPL version 2',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['intranett'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'collective.ATClamAV',
          'collective.flag',
          'experimental.catalogqueryplan',
          'iw.rejectanonymous',
          'munin.zope',
          'PIL',
          'Plone',
          'plone.app.caching',
          'plone.app.discussion',
          'plone.app.testing',
          'Products.CMFQuickInstallerTool',
          'Products.GenericSetup',
          'Products.PloneFormGen',
          'Products.PloneHotfix20110720',
          'Products.PloneTestCase',
          'Products.signalstack',
          'unittest2',
          'Zope2',
          'zope.component',
          'zope.interface',
          'z3c.unconfigure',
          'intranett.theme',
      ],
      entry_points="""
      [zopectl.command]
      create_site = intranett.policy.commands:create_site
      upgrade = intranett.policy.commands:upgrade
      """)
