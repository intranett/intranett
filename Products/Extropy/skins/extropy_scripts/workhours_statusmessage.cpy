## Controller Python Script "workhours_statusmessage"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=
##title=
##

message = "Changed worked hours."

context.plone_utils.addPortalMessage(message)
return state
