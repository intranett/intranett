from setuptools import setup, find_packages

version = '1.0'

setup(name='intranett.tour',
      version=version,
      description="Amberjack tour for intranett.no",
      long_description="",
      classifiers=[
        "Programming Language :: Python",
        ],
      keywords='',
      author='',
      author_email='',
      url='http://intranett.no',
      license='Provate',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['intranett'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'collective.amberjack.core',
          'collective.amberjack.portlet'
      ],
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
