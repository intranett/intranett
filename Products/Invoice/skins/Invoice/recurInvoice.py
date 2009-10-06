from Products.CMFPlone import PloneMessageFactory as _
newurl = context.createRecurrence()
context.plone_utils.addPortalMessage(_(u'New invoice created. Now make sure to edit the contents of it'))
context.REQUEST.RESPONSE.redirect(newurl)
