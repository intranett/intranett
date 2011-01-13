from setuptools import setup, find_packages

version = '2.0dev'

setup(name='intranett.theme',
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
      url='http://www.jarn.com',
      license='GPL version 2',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['intranett'],
      include_package_data=True,
      zip_safe=False,
      extras_require=dict(test=[
        'intranett.policy >= 0.4',
      ]),
      install_requires=[
          'setuptools',
          'z3c.jbot'
      ],
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
