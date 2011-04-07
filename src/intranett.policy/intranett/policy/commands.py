import logging
import os
import sys
import imaplib
import email
import time
from optparse import OptionParser

import transaction
from AccessControl.SecurityManagement import newSecurityManager
from Testing import makerequest
from zope.site.hooks import setHooks
from zope.site.hooks import setSite


logger = logging.getLogger()


def _setup(app, site=None):
    """Set up our environment.

    Create a request, log in as admin and set the traversal hooks on the site.

    """
    root = makerequest.makerequest(app)

    # Login as admin
    admin = root.acl_users.getUserById('admin')
    if admin is None:
        logger.error("No user called `admin` found in the database. "
            "Use --rootpassword to create one.")
        sys.exit(1)

    # Wrap the admin in the right context; from inside the site if we have one
    if site is not None:
        admin = admin.__of__(site.acl_users)
    else:
        admin = admin.__of__(root.acl_users)
    newSecurityManager(None, admin)

    # Set up local site manager
    if site is not None:
        setHooks()
        setSite(site)

    return root


def create_site(app, args):
    # Display all messages on stderr
    logger.setLevel(logging.INFO)
    logger.handlers[0].setLevel(logging.INFO)

    parser = OptionParser()
    parser.add_option('-f', '--force', action='store_true', default=False,
        help='Force creation of a site when one already exists.')
    parser.add_option('-r', '--rootpassword', default=None,
        help='Create a admin user in the Zope root with the given password.')
    parser.add_option('-t', '--title',
        default=os.environ.get('INTRANETT_DOMAIN', 'intranett.no'),
        help='The title for the new site. The default can also be set with '
            'the INTRANETT_DOMAIN environment variable. [default: "%default"]')
    parser.add_option('-l', '--language', default='no',
        help='The language used in the new site. [default: "%default"]')
    (options, args) = parser.parse_args(args=args)

    if options.rootpassword:
        acl = app.acl_users
        users = getattr(acl, 'users', None)
        if not users:
            # Non-PAS folder from a fresh database
            app.acl_users._doAddUser('admin', options.rootpassword,
                ['Manager'], [])

    existing = app.objectIds('Plone Site')
    if existing:
        if not options.force:
            logger.error('Plone site already exists. '
                'Use --force to replace it.')
            sys.exit(1)
        else:
            for id_ in existing:
                del app[id_]
                logger.info('Removed existing Plone site %r.' % id_)
            app._p_jar.db().cacheMinimize()

    root = _setup(app)

    request = root.REQUEST
    request.form = {
        'extension_ids': ('intranett.policy:default', ),
        'form.submitted': True,
        'title': options.title,
        'language': options.language,
    }
    from intranett.policy.browser.admin import AddIntranettSite
    addsite = AddIntranettSite(root, request)
    addsite()
    transaction.get().note('Added new Plone site.')
    transaction.get().commit()
    logger.info('Added new Plone site.')


def upgrade(app, args):
    # Display all messages on stderr
    logger.setLevel(logging.DEBUG)
    logger.handlers[0].setLevel(logging.DEBUG)

    existing = app.objectValues('Plone Site')
    site = existing and existing[0] or None
    if site is None:
        logger.error("No Plone site found in the database.")
        sys.exit(1)

    _setup(app, site)

    from intranett.policy.config import config

    logger.info("Starting the upgrade.\n\n")
    setup = site.portal_setup
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

    existing = app.objectValues('Plone Site')
    site = existing and existing[0] or None
    if site is None:
        logger.error("No Plone site found in the database.")
        sys.exit(1)

    _setup(app, site)

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
    for num in data[0].split():
        typ, data = imap.fetch(num, '(RFC822)')
        walk_parts(num,email.message_from_string(data[0][1]),dropbox)
        imap.store(num, "+FLAGS.SILENT", '(\\Deleted)')
        transaction.get().note('Downloaded attachements from emails.')
        transaction.get().commit()
