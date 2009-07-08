## Controller Python Script "split_task"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=targetPhase=None
##title=Split a task
##

o = context.spawnTask(targetPhase)

if o is None:
    raise Exception, "Failure spawning task"

message = 'Spawned task from %s.' % context.Title()

state.setStatus('success_no_edit')

return state.set(context=o, portal_status_message=message)
