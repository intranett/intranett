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

msg = "Changed worked hours."

return state.set( portal_status_message=msg)
