import logging
import os
import sys
import imaplib
import email
import time
logger = logging.getLogger()


def create_site(app, args):
    # Display all messages on stderr
    logger.setLevel(logging.INFO)
    logger.handlers[0].setLevel(logging.INFO)

    force = '--force' in args or '-f' in args
    from Products.CMFPlone.Portal import PloneSite
    existing = [p.getId() for p in app.values() if isinstance(p, PloneSite)]

    root_arg = [a for a in args if a.startswith('--rootpassword')]
    if any(root_arg):
        password = root_arg[0].split('=')[1].strip()
        acl = app.acl_users
        users = getattr(acl, 'users', None)
        if not users:
            # Non-PAS folder from a fresh database
            app.acl_users._doAddUser('admin', password, ['Manager'], [])

    if any(existing):
        if not force:
            logger.error('Plone site already exists.')
            sys.exit(1)
        else:
            for id_ in existing:
                del app[id_]
            app._p_jar.db().cacheMinimize()
            logger.info('Removed existing Plone site.')

    from Testing import makerequest
    root = makerequest.makerequest(app)
    request = root.REQUEST

    # Login as admin
    from AccessControl.SecurityManagement import newSecurityManager
    admin = root.acl_users.getUserById('admin')
    if admin is None:
        logger.error("No user called `admin` found in the database.")
        sys.exit(1)
    newSecurityManager(None, admin)

    title = os.environ.get('INTRANETT_DOMAIN', 'intranett.no')
    title_arg = [a for a in args if a.startswith('--title')]
    if any(title_arg):
        targ = title_arg[0].split('=')[1].strip()
        if targ:
            title = targ

    language = 'no'
    lang_arg = [a for a in args if a.startswith('--language')]
    if any(lang_arg):
        language = lang_arg[0].split('=')[1].strip()

    request.form = {
        'extension_ids': ('intranett.policy:default', ),
        'form.submitted': True,
        'title': title,
        'language': language,
    }
    from intranett.policy.browser.admin import AddIntranettSite
    addsite = AddIntranettSite(root, request)
    addsite()
    import transaction
    transaction.get().note('Added new Plone site.')
    transaction.get().commit()
    logger.info('Added new Plone site.')


def upgrade(app, args):
    # Display all messages on stderr
    logger.setLevel(logging.DEBUG)
    logger.handlers[0].setLevel(logging.DEBUG)
    # Make app.REQUEST available
    from Testing import makerequest
    root = makerequest.makerequest(app)

    from Products.CMFPlone.Portal import PloneSite
    site_ids = [p.getId() for p in root.values() if isinstance(p, PloneSite)]
    site_id = site_ids[0]

    site = root.get(site_ids[0], None)
    if site is None:
        logger.error("No site called `%s` found in the database." % site_id)
        sys.exit(1)

    # Login as admin
    from AccessControl.SecurityManagement import newSecurityManager
    admin = root.acl_users.getUserById('admin')
    if admin is None:
        logger.error("No user called `admin` found in the database.")
        sys.exit(1)
    newSecurityManager(None, admin)

    # Set up local site manager
    from zope.site.hooks import setHooks
    from zope.site.hooks import setSite
    setHooks()
    setSite(site)
    setup = site.portal_setup

    import transaction
    from intranett.policy.config import config

    logger.info("Starting the upgrade.\n\n")
    config.run_all_upgrades(setup)
    logger.info("Ran upgrade steps.")

    # Recook resources, as some CSS/JS/KSS files might have changed.
    # TODO: We could try to determine if this is needed in some way
    site.portal_javascripts.cookResources()
    site.portal_css.cookResources()
    site.portal_kss.cookResources()
    logger.info("Resources recooked.")

    transaction.get().note('Upgraded profiles and recooked resources.')
    transaction.get().commit()
    sys.exit(0)


def walk_parts(msgnum,msg,folder,date=None,count=0,addr=None):
    if date==None:
        date = msg['Date'] or 'Thu, 18 Sep 2006 12:02:27 +1000'
        date = time.strftime('%Y_%m_%d.%T', email.Utils.parsedate(date))
    if addr==None:
        addr = email.Utils.parseaddr(msg['From'])[1]
    for part in msg.walk():
        if part.is_multipart():
            continue
        dtypes = part.get_params(None, 'Content-Disposition')
        if not dtypes:
            if part.get_content_type() == 'text/plain':
                continue
            ctypes = part.get_params()
            if not ctypes:
                continue
            for key,val in ctypes:
                if key.lower() == 'name':
                    filename = val
                    break
            else:
                continue
        else:
            attachment,filename = None,None
            for key,val in dtypes:
				key = key.lower()
				if key == 'filename':
					filename = val
				if key == 'attachment':
					attachment = 1
            if not attachment:
                continue
            print filename
        try:
            data = part.get_payload(decode=1)
        except:
            typ, val = sys.exc_info()[:2]
            print "Message %s attachment decode error: %s for %s ``%s''" % (msgnum, str(val), part.get_content_type(), filename)
            continue
        if not data:
            print "Could not decode attachment %s for %s" % (part.get_content_type(), filename)
            continue

        if type(data) is type(msg):
            count = walk_parts(msgnum,data,folder, addr=addr, date=date, count=count )
            continue

        idx = folder.invokeFactory("File",id=filename)
        f = folder[idx].getFile()
        f.setFilename(filename)
        f.setTitle(filename)
        f.setContentType(part.get_content_type())
        f.setDescription("Recieved on email on %s from %s"%(date,addr))
        blob = f.getBlob()
        blobfile = blob.open("w")
        blobfile.writelines(data)
        blobfile.close()
        count += 1
        print count
	return count

def download_email(app,args):
    logger.setLevel(logging.DEBUG)
    logger.handlers[0].setLevel(logging.DEBUG)
    # Make app.REQUEST available
    from Testing import makerequest
    root = makerequest.makerequest(app)

    from Products.CMFPlone.Portal import PloneSite
    site_ids = [p.getId() for p in root.values() if isinstance(p, PloneSite)]
    site_id = site_ids[0]

    site = root.get(site_ids[0], None)
    if site is None:
        logger.error("No site called `%s` found in the database." % site_id)
        sys.exit(1)

    # Login as admin
    from AccessControl.SecurityManagement import newSecurityManager
    admin = root.acl_users.getUserById('admin')
    if admin is None:
        logger.error("No user called `admin` found in the database.")
        sys.exit(1)
    newSecurityManager(None, admin)

    # Set up local site manager
    from zope.site.hooks import setHooks
    from zope.site.hooks import setSite
    setHooks()
    setSite(site)
    if not "dropbox" in site.keys():
        print "no dropbox"
        return
    dropbox = site["dropbox"]
    if not dropbox.portal_type=="Folder":
        return
    imap = imaplib.IMAP4_SSL("imap.gmail.com")
    imap.login("printer@jarn.com","54+Ov@RG")
    imap.select("INBOX")
    typ, data = imap.search(None, '(TO "jarn-intranett@intranett.no")')
    import transaction
    for num in data[0].split():
        typ, data = imap.fetch(num, '(RFC822)')
        walk_parts(num,email.message_from_string(data[0][1]),dropbox)
        imap.store(num, "+FLAGS.SILENT", '(\\Deleted)')
        transaction.get().note('Downloaded attachements from emails.')
        transaction.get().commit()
