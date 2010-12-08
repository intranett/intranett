from setuptools import setup, find_packages

version = '1.2'

setup(name='intranett.policy',
      version=version,
      description="",
      long_description=open("README.txt").read() + "\n" +
                       open("CHANGES.txt").read(),
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
          'collective.monkeypatcher',
          'experimental.catalogqueryplan',
          'munin.zope',
          'Plone',
          'plone.app.caching',
          'plone.app.discussion',
          'plone.app.testing',
          'Products.CMFQuickInstallerTool',
          'Products.GenericSetup',
          'Products.PloneFormGen',
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
