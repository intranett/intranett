from setuptools import setup, find_packages

version = '0.2'

setup(name='intranett.theme',
      version=version,
      description="Basic theme providing base fonts, typography, \
                   rhythm for intranett.no projects. Particular \
                   projects' specific visual themes are going to \
                   be built on top of this base theme.",
      long_description=open("README.txt").read() + "\n" +
                       open("CHANGES.txt").read(),
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
