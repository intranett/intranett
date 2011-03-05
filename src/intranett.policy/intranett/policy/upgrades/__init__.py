from Acquisition import aq_get

from intranett.policy.config import config


def run_upgrade(setup, profile_id=config.policy_profile):
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
    run_upgrade(setup, setup.getBaselineContextID().lstrip('profile-'))
    run_upgrade(setup, config.theme_profile)
    run_upgrade(setup)
