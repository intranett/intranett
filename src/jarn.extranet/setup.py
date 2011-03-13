from setuptools import setup, find_packages

version = '1.0'

setup(name='jarn.extranet',
      version=version,
      description="Extranet for Jarn and customers",
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
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['jarn'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
      ],
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
