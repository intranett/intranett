from Acquisition import aq_get


def null_upgrade_step(tool):
    """This is a null upgrade, use it when nothing happens."""
    pass


def run_upgrade(setup, profile_id=u"intranett.policy:default"):
    request = aq_get(setup, 'REQUEST')
    request.form['profile_id'] = profile_id

    upgrades = setup.listUpgrades(profile_id)

    steps = []
    for u in upgrades:
        if isinstance(u, list): # pragma: no cover
            steps.extend([s['id'] for s in u])
        else:
            steps.append(u['id'])

    request.form['upgrades'] = steps
    setup.manage_doUpgrades(request=request)
