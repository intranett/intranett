import logging
import os
import sys
from optparse import OptionParser

import transaction
from AccessControl.SecurityManagement import newSecurityManager
from zope.site.hooks import setHooks
from zope.site.hooks import setSite


logger = logging.getLogger()


def _setup(app, site=None):
    """Set up our environment.

    Create a request, log in as admin and set the traversal hooks on the site.

    """
    from Testing import makerequest # Do not import this at the module level!
    app = makerequest.makerequest(app)

    # Login as admin
    admin = app.acl_users.getUserById('admin')
    if admin is None:
        logger.error("No user called `admin` found in the database. "
            "Use --rootpassword to create one.")
        sys.exit(1)

    # Wrap the admin in the right context; from inside the site if we have one
    if site is not None:
        admin = admin.__of__(site.acl_users)
        site = app[site.getId()]
    else:
        admin = admin.__of__(app.acl_users)
    newSecurityManager(None, admin)

    # Set up local site manager
    if site is not None:
        setHooks()
        setSite(site)

    return (app, site)


def create_site(app, args):
    # Display all messages on stderr
    logger.setLevel(logging.INFO)
    logger.handlers[0].setLevel(logging.INFO)

    parser = OptionParser()
    parser.add_option('-f', '--force', action='store_true', default=False,
        help='Force creation of a site when one already exists.')
    parser.add_option('-r', '--rootpassword', default=None,
        help='Create a admin user in the Zope root with the given password.')
    parser.add_option('-t', '--title',
        default=os.environ.get('INTRANETT_DOMAIN', 'intranett.no'),
        help='The title for the new site. The default can also be set with '
            'the INTRANETT_DOMAIN environment variable. [default: "%default"]')
    parser.add_option('-l', '--language', default='no',
        help='The language used in the new site. [default: "%default"]')
    (options, args) = parser.parse_args(args=args)

    if options.rootpassword:
        acl = app.acl_users
        users = getattr(acl, 'users', None)
        if not users:
            # Non-PAS folder from a fresh database
            app.acl_users._doAddUser('admin', options.rootpassword,
                ['Manager'], [])

    existing = app.objectIds('Plone Site')
    if existing:
        if not options.force:
            logger.error('Plone site already exists. '
                'Use --force to replace it.')
            sys.exit(1)
        else:
            for id_ in existing:
                del app[id_]
                logger.info('Removed existing Plone site %r.' % id_)
            app._p_jar.db().cacheMinimize()

    app, _ = _setup(app)

    request = app.REQUEST
    request.form = {
        'extension_ids': ('intranett.policy:default', ),
        'form.submitted': True,
        'title': options.title,
        'language': options.language,
    }
    from intranett.policy.browser.admin import AddIntranettSite
    addsite = AddIntranettSite(app, request)
    addsite()
    transaction.get().note('Added new Plone site.')
    transaction.get().commit()
    logger.info('Added new Plone site.')


def upgrade(app, args):
    # Display all messages on stderr
    logger.setLevel(logging.DEBUG)
    logger.handlers[0].setLevel(logging.DEBUG)

    existing = app.objectValues('Plone Site')
    site = existing and existing[0] or None
    if site is None:
        logger.error("No Plone site found in the database.")
        sys.exit(1)

    _, site = _setup(app, site)

    from intranett.policy.config import config

    logger.info("Starting the upgrade.\n\n")
    setup = site.portal_setup
    config.run_all_upgrades(setup)
    logger.info("Ran upgrade steps.")

    # Recook resources, as some CSS/JS/KSS files might have changed.
    # TODO: We could try to determine if this is needed in some way
    site.portal_javascripts.cookResources()
    site.portal_css.cookResources()
    site.portal_kss.cookResources()
    logger.info("Resources recooked.")

    transaction.get().note('Upgraded profiles and recooked resources.')
    transaction.get().commit()
    sys.exit(0)
