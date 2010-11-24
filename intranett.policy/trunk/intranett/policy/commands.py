import logging
import sys

logger = logging.getLogger()


def compare_profile_versions(setup, profile_id):
    current = setup.getVersionForProfile(profile_id)
    current = tuple(current.split('.'))
    last = setup.getLastVersionForProfile(profile_id)
    return current == last


def upgrade(app, args=None):
    # Display all messages on stderr
    logger.setLevel(logging.DEBUG)
    logger.handlers[0].setLevel(logging.DEBUG)

    from Testing import makerequest
    root = makerequest.makerequest(app)
    site = root.get('Plone', None)
    if site is None:
        logger.error("No site called `Plone` found in the database.")
        sys.exit(1)

    from zope.site.hooks import setHooks
    from zope.site.hooks import setSite
    setHooks()
    setSite(site)
    setup = site.portal_setup

    import transaction
    from intranett.policy.config import POLICY_PROFILE
    from intranett.policy.config import THEME_PROFILE
    from intranett.policy.upgrades import run_upgrade

    logger.info("Starting the upgrade.\n\n")
    run_upgrade(setup, u"intranett.theme:default")
    logger.info("Ran theme upgrade.")
    run_upgrade(setup)
    logger.info("Ran policy upgrade.")

    # Check if we reached the current version
    policy_updated = compare_profile_versions(setup, POLICY_PROFILE)
    theme_updated = compare_profile_versions(setup, THEME_PROFILE)

    if policy_updated and theme_updated:
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
