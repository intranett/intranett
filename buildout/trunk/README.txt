Documentation
=============

Tests
-----

You can run tests for all packages at once using::

  bin/test

In order to run coverage tests, use::

  bin/coverage
  bin/report-html

You can view the coverage results in the htmlcov directory via::

  open htmlcov/index.html

Working on a ticket
-------------------

If you work on a non-trivial story ticket, you should create a separate
config file and branch the code you need to change. The trunk of each
distribution should always be in a releasable state to the production
environment.

As a convention we use the ticket number and a short word or two to describe
each ticket.

For example, if you want to work on ticket #82, called ``Special view for the
frontpage``, here's the steps you should take::

  svn cp 0-ticketname.cfg 82-frontpage.cfg

In the beginning you only need a branch of ``intranett.theme``, so you create
one::

  svn cp https://svn.jarn.com/jarn/intranett.no/intranett.theme/trunk \
         https://svn.jarn.com/jarn/intranett.no/intranett.theme/branches/82-frontpage

Edit the ``82-frontpage.cfg`` to point to the new branch and run::

  bin/buildout -c 82-frontpage.cfg

You are now working against your set of branches and can pull in additional
dependencies if you want to. Other people can work with you on the same ticket
by using the same config.

After the ticket is done, all tests are written, it's been tested TTW,
upgrade notes or automatic steps are in place and quality assurance has been
performed, you can merge your changes back to the trunk and integrate any
required changes into the buildout files.
