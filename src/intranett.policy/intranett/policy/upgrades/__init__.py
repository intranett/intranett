from Acquisition import aq_get

from intranett.policy.config import config
from intranett.policy.config import BASE_PROFILE
from intranett.policy.config import POLICY_PROFILE
from intranett.policy.config import THEME_PROFILE


def compare_profile_versions(setup, profile_id):
    if profile_id == POLICY_PROFILE:
        current = config.last_upgrade_to()
    else:
        current = setup.getVersionForProfile(profile_id)
    current = tuple(current.split('.'))
    last = setup.getLastVersionForProfile(profile_id)
    return current == last


def run_upgrade(setup, profile_id=POLICY_PROFILE):
    request = aq_get(setup, 'REQUEST')
    request['profile_id'] = profile_id

    upgrades = setup.listUpgrades(profile_id)

    steps = []
    for u in upgrades:
        if isinstance(u, list): # pragma: no cover
            steps.extend([s['id'] for s in u])
        else:
            steps.append(u['id'])

    request.form['upgrades'] = steps
    setup.manage_doUpgrades(request=request)


def run_all_upgrades(setup):
    run_upgrade(setup, BASE_PROFILE)
    run_upgrade(setup, THEME_PROFILE)
    run_upgrade(setup)

    base_updated = compare_profile_versions(setup, BASE_PROFILE)
    theme_updated = compare_profile_versions(setup, THEME_PROFILE)
    policy_updated = compare_profile_versions(setup, POLICY_PROFILE)
    return all([base_updated, theme_updated, policy_updated])
