from setuptools import setup, find_packages

version = '0.7'

setup(name='Products.Extropy',
      version=version,
      description="",
      long_description=open("README.txt").read() + "\n" +
                       open("CHANGES.txt").read(),
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
          'experimental.catalogqueryplan',
          'plone.app.blob',
          'Products.TinyMCE',
          'Products.Invoice',
          'Products.Maps',
          'Products.Memo',
          'Products.signalstack',
          'jarn.intranet.tracportlet',
      ],
      )
