## Script (Python) "author"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=Redirect to the canonical author page

from Products.PythonScripts.standard import url_quote
from Products.CMFCore.utils import getToolByName
from intranett.policy.utils import getMembersFolderId

request = context.REQUEST
portal_url = getToolByName(context, 'portal_url')()

author = ''
if len(request.traverse_subpath) > 0:
    author = request.traverse_subpath[0]
else:
    author = request.get('author', '')

result = portal_url + '/' + url_quote(getMembersFolderId())
if author:
    result = result + '/' + url_quote(author)

return request.response.redirect(result)
