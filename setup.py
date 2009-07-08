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
          'Products.DataGridField',
          'Products.Maps',
          'Products.MaildropHost',
          'Products.Memo',
          'Products.SecureMaildropHost',
          'Products.signalstack',
          'experimental.catalogqueryplan',
          'python-gettext',
      ],
      )
