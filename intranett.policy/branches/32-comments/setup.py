from setuptools import setup, find_packages

version = '0.1'

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
      license='Private',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['intranett'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'collective.testcaselayer',
          'experimental.catalogqueryplan',
          'Plone',
          'plonetheme.sunburst',
          'Products.CMFQuickInstallerTool',
          'Products.GenericSetup',
          'Products.PloneFormGen',
          'Products.PloneTestCase',
          'Zope2',
          'zope.component',
          'zope.interface',
          'intranett.theme',
      ],
      )
