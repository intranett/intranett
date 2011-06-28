##parameters=
# Go to frontpage
context.REQUEST.RESPONSE.setCookie('editbar_opened', path='/', value='1')
context.REQUEST.RESPONSE.redirect(context.portal_url())
