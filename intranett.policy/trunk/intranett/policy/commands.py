import logging
import sys

logger = logging.getLogger()


def upgrade(app, args=None):
    # Display all messages on stderr
    logger.setLevel(logging.DEBUG)
    logger.handlers[0].setLevel(logging.DEBUG)

    # Make app.REQUEST available
    from Testing import makerequest
    root = makerequest.makerequest(app)
    site = root.get('Plone', None)
    if site is None:
        logger.error("No site called `Plone` found in the database.")
        sys.exit(1)

    # Set up local site manager
    from zope.site.hooks import setHooks
    from zope.site.hooks import setSite
    setHooks()
    setSite(site)
    setup = site.portal_setup

    import transaction
    from intranett.policy.upgrades import run_all_upgrades

    logger.info("Starting the upgrade.\n\n")
    all_finished = run_all_upgrades(setup)
    logger.info("Ran upgrade steps.")

    if all_finished:
        logger.info("Upgrade successful.")

        # Recook resources, as some CSS/JS/KSS files might have changed.
        # TODO: We could try to determine if this is needed in some way
        site.portal_javascripts.cookResources()
        site.portal_css.cookResources()
        site.portal_kss.cookResources()
        logger.info("Resources recooked.")

        transaction.get().note('Upgraded profiles and recooked resources.')
        transaction.get().commit()
        sys.exit(0)

    transaction.get().abort()
    logger.error("Upgrade didn't reach current versions - aborted.")
    sys.exit(1)
