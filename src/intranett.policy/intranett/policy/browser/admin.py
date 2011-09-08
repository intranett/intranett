from Products.CMFPlone.browser.admin import AddPloneSite
from Products.CMFPlone.browser.admin import Overview
from Products.CMFPlone.factory import _DEFAULT_PROFILE
from Products.CMFPlone.factory import addPloneSite


class IntranettOverview(Overview):
    pass


class AddIntranettSite(AddPloneSite):

    default_extension_profiles = (
        'intranett.policy:default',
        )

    def __call__(self):
        context = self.context
        form = self.request.form
        submitted = form.get('form.submitted', False)
        if submitted:
            site = addPloneSite(
                context, 'Plone',
                profile_id=_DEFAULT_PROFILE,
                extension_ids=form.get('extension_ids',
                    (u'intranett.policy:default',)),
                setup_content=False,
                default_language=form.get('language', 'no'),
                )
            return self.request.response.redirect(site.absolute_url())

        return self.index()
