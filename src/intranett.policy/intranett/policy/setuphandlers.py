from Acquisition import aq_get
from plutonian.gs import import_step
from Products.CMFCore.utils import getToolByName
from zope.component import queryMultiAdapter
from zope.component import queryUtility
from zope.i18n import translate
from zope.interface import alsoProvides

from intranett.policy.config import config


def set_profile_version(site):
    setup = getToolByName(site, 'portal_setup')
    setup.setLastVersionForProfile(
        config.policy_profile, config.last_upgrade_to())


def setup_locale(site):
    request = aq_get(site, 'REQUEST', None)
    language = 'no'
    if request is not None:
        language = request.form.get('language', 'no')
    site.setLanguage(language)
    tool = getToolByName(site, "portal_languages")
    tool.manage_setLanguageSettings(language,
        [language],
        setUseCombinedLanguageCodes=False,
        startNeutral=False)

    calendar = getToolByName(site, "portal_calendar")
    calendar.firstweekday = 0


def ensure_workflow(site):
    # Force the default content into the correct workflow
    from plone.app.workflow.remap import remap_workflow
    # No longer needed, we think.  Leaving here for a bit just in case.
    # Matthew and Stefan.
    # 
    #remap_workflow(site,
    #               type_ids=('Document', 'Folder', 'Topic'),
    #s               chain=('intranett_workflow', 'workspace_workflow'))


def disable_contentrules(site):
    from plone.contentrules.engine.interfaces import IRuleStorage
    rule = queryUtility(IRuleStorage)
    if rule is not None:
        rule.active = False


def disallow_sendto(site):
    perm_id = 'Allow sendto'
    site.manage_permission(perm_id, roles=['Manager'], acquire=0)


def disable_collections(site):
    # Once collections are usable or we have a SiteAdmin role this should be
    # changed (both depend on Plone 4.1)
    perm_id = 'Add portal topics'
    site.manage_permission(perm_id, roles=[], acquire=0)
    perm_id = 'plone.portlet.collection: Add collection portlet'
    site.manage_permission(perm_id, roles=[], acquire=0)


def disable_portlets(site):
    from plone.portlets.interfaces import IPortletType
    from zope.component import getUtilitiesFor

    disabled = ['portlets.Calendar', 'portlets.Classic', 'portlets.Login',
                'portlets.Review', 'plone.portlet.collection.Collection']

    for info in getUtilitiesFor(IPortletType):
        if info[0] in disabled:
            p = info[1]
            # We remove the IColumn specification here, which makes the
            # portlets not addable for anything
            p.for_ = []
            p._p_changed = True


def setup_default_groups(site):
    gtool = getToolByName(site, 'portal_groups')
    # We could add more groups like this:
    # gtool.addGroup('Users', title='Users', roles=['Member'])
    gtool.removeGroups(['Administrators', 'Reviewers', 'Site Administrators'])


def setup_reject_anonymous(site):
    from iw.rejectanonymous import IPrivateSite
    # Used both as a setup and upgrade handler
    portal = getToolByName(site, 'portal_url').getPortalObject()
    alsoProvides(portal, IPrivateSite)


def setup_members_folder(site):
    from Products.CMFPlone.utils import _createObjectByType
    from intranett.policy.config import MEMBERS_FOLDER_ID
    fti = getToolByName(site, 'portal_types')['MembersFolder']
    title = translate(fti.Title(), target_language=site.Language())
    portal = getToolByName(site, 'portal_url').getPortalObject()
    _createObjectByType('MembersFolder', portal, id=MEMBERS_FOLDER_ID,
        title=title)
    # we fill the request with some values in commands.py create_site
    # don't let those interfere in the processForm call
    request = aq_get(portal, 'REQUEST', None)
    if request is not None:
        request.form['title'] = title
    portal[MEMBERS_FOLDER_ID].processForm() # Fire events
    workflow = getToolByName(portal, 'portal_workflow')
    workflow.doActionFor(portal[MEMBERS_FOLDER_ID], 'publish')


def setup_personal_folder(site):
    from plone.portlets.interfaces import ILocalPortletAssignmentManager
    from plone.portlets.interfaces import IPortletManager
    from Products.CMFPlone.utils import _createObjectByType
    from intranett.policy.config import PERSONAL_FOLDER_ID
    from intranett.policy import IntranettMessageFactory as _
    personal_folder_title = _(u'Personal folders')
    title = translate(personal_folder_title, target_language=site.Language())
    portal = getToolByName(site, 'portal_url').getPortalObject()
    _createObjectByType('Folder', portal, id=PERSONAL_FOLDER_ID,
        title=title)
    # we fill the request with some values in commands.py create_site
    # don't let those interfere in the processForm call
    request = aq_get(portal, 'REQUEST', None)
    if request is not None:
        request.form['title'] = title
    folder = portal[PERSONAL_FOLDER_ID]
    folder.setExcludeFromNav(True)
    folder.processForm() # Fire events
    workflow = getToolByName(portal, 'portal_workflow')
    workflow.doActionFor(folder, 'publish')
    # Block all portlets
    for manager_name in ('plone.leftcolumn', 'plone.rightcolumn'):
        manager = queryUtility(IPortletManager, name=manager_name)
        if manager is not None:
            assignable = queryMultiAdapter((folder, manager),
                ILocalPortletAssignmentManager)
            assignable.setBlacklistStatus('context', True)
            assignable.setBlacklistStatus('group', True)
            assignable.setBlacklistStatus('content_type', True)


def enable_secure_cookies(context):
    acl = aq_get(context, 'acl_users')
    acl.session._updateProperty('secure', True)


def ignore_link_integrity_exceptions(site):
    error_log = aq_get(site, 'error_log')
    props = error_log.getProperties()
    exceptions = props['ignored_exceptions']
    exceptions = exceptions + ('LinkIntegrityNotificationException', )
    error_log.setProperties(props['keep_entries'],
        ignored_exceptions=tuple(sorted(set(exceptions))))


def enable_link_by_uid(site):
    from plone.outputfilters.setuphandlers import \
        install_mimetype_and_transforms
    tiny = getToolByName(site, 'portal_tinymce')
    tiny.link_using_uids = True
    install_mimetype_and_transforms(site)


def open_ext_links_in_new_window(site):
    jstool = getToolByName(site, 'portal_javascripts')
    jstool.getResource('mark_special_links.js').setEnabled(True)
    jstool.cookResources()


def restrict_siteadmin(site):
    perm_ids = (
        'Content rules: Manage rules',
        'FTP access',
        'Plone Site Setup: Overview',
        'Plone Site Setup: Calendar',
        'Plone Site Setup: Editing',
        'Plone Site Setup: Filtering',
        'Plone Site Setup: Imaging',
        'Plone Site Setup: Language',
        'Plone Site Setup: Mail',
        'Plone Site Setup: Markup',
        'Plone Site Setup: Navigation',
        'Plone Site Setup: Search',
        'Plone Site Setup: Security',
        'Plone Site Setup: Site',
        'Plone Site Setup: Themes',
        'Plone Site Setup: TinyMCE',
        'Plone Site Setup: Types',
        'Sharing page: Delegate Reviewer role',
        'Undo changes',
        'Use Database Methods',
        'Use external editor',
        'View management screens',
        'WebDAV access',
        )
    for perm_id in perm_ids:
        site.manage_permission(perm_id, roles=['Manager'], acquire=0)


# TODO the default can go with plutonian > 0.1a2
@import_step(depends=('plone-final', 'workflow', ))
def various(context):
    # Only run step if a flag file is present (e.g. not an extension profile)
    if context.readDataFile('intranett-policy-various.txt') is None:
        return
    site = context.getSite()
    set_profile_version(site)
    setup_locale(site)
    ensure_workflow(site)
    disable_contentrules(site)
    disallow_sendto(site)
    disable_collections(site)
    disable_portlets(site)
    setup_default_groups(site)
    setup_reject_anonymous(site)
    setup_members_folder(site)
    setup_personal_folder(site)
    enable_secure_cookies(site)
    ignore_link_integrity_exceptions(site)
    enable_link_by_uid(site)
    open_ext_links_in_new_window(site)
    restrict_siteadmin(site)
