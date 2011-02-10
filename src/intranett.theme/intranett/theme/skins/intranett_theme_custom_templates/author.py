## Script (Python) "author"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=Redirect to the canonical author page

from Products.CMFCore.utils import getToolByName

request = context.REQUEST
portal_url = getToolByName(context, 'portal_url')()

author = ''
if len(request.traverse_subpath) > 0:
    author = request.traverse_subpath[0]
else:
    author = request.get('author', '')

result = portal_url + '/user'
if author:
    result = result + '/' + author

return request.response.redirect(result)
