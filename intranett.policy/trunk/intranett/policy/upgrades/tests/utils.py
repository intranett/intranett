POLICY_PROFILE = u"intranett.policy:default"
CMF_PROFILE = u"Products.CMFDefault:default"
PAI_PROFILE = u"plone.app.iterate:plone.app.iterate"


def ensure_no_addon_upgrades(setup):
    profiles = set(setup.listProfilesWithUpgrades())
    # Don't test our own profile twice
    profiles.remove(POLICY_PROFILE)
    # We don't care about the CMFDefault profile in Plone
    profiles.remove(CMF_PROFILE)
    # The iterate profile has a general reinstall profile in it, we ignore
    # it since we don't use iterate
    profiles.remove(PAI_PROFILE)
    upgrades = {}
    for profile in profiles:
        upgrades[profile] = setup.listUpgrades(profile)
    return upgrades
