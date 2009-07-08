## Controller Python Script "claim_task"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=
##title=Claim current task
##

context.claimTask()
state.setStatus('success')
return state.set(portal_status_message='Task claimed')
