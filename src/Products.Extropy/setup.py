from setuptools import setup, find_packages

version = '2.0dev'

setup(name='Products.Extropy',
      version=version,
      description="",
      long_description=open("README.txt").read(),
      classifiers=[
        "Framework :: Plone",
        ],
      keywords='',
      author='Jarn AS',
      author_email='info@jarn.com',
      url="",
      license='Private',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['Products'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'intranett.theme',
          'jarn.extranet',
          'Products.Invoice',
          'RelStorage',
      ],
      )
