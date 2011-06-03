import os
import os.path
import subprocess

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
    proc = subprocess.Popen(['git', 'log', '-n 1', '--pretty="%h %ci"'],
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    proc.wait()
    out = proc.stdout.read()
    info = out.strip('\n"').split()
    revision, date, time, tz = info
    version += 'dev-' + revision + '-' + date


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
          'iw.rejectanonymous',
          'munin.zope',
          'PIL',
          'Plone',
          'plone.app.caching',
          'plone.app.discussion',
          'plone.app.testing',
          'plone.formwidget.autocomplete',
          'plone.principalsource',
          'plutonian',
          'Products.CMFQuickInstallerTool',
          'Products.GenericSetup',
          'Products.PloneFormGen',
          'unittest2',
          'Zope2',
          'zope.component',
          'zope.interface',
          'intranett.theme',
      ],
      entry_points="""
      [zopectl.command]
      create_site = intranett.policy.commands:create_site
      create_site_admin = intranett.policy.commands:create_site_admin
      upgrade = intranett.policy.commands:upgrade
      """)
