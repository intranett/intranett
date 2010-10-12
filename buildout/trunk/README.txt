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

Procedures
----------

For this project we adhere to our highest professional standards. You should
have an idea of what this means. Some of these include:

- The code on trunk is always in a production ready state.

- We don't deploy code from version control systems, but make releases.

- We work on branches for features and only merge them once they are *really*
  done, including translations, UI testing, documentation or whatever else.

- We keep 100% test coverage for all our code. This makes sure we don't have
  SyntaxErrors or other stupid mistakes anywhere. We force ourselves to do
  this by treating missing coverage in the same way as broken tests.

- We keep story tickets and define acceptance criteria. Ideally those criteria
  are directly transferable into functional tests.

- If we cannot solve a problem or write tests for something, we ask others to
  help us, instead of ignoring the problem - even if that means we cannot
  finish something as early as we'd like to.

- ... to be continued ...
