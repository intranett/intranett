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

If you work on a non-trivial story ticket, you should create a branch of this
buildout. The Git master should always be in a releasable state to the
production environment.

As a convention we use the ticket number and a short word or two to describe
each ticket.

For example, if you want to work on ticket #82, called ``Special view for the
frontpage``, here's the steps you should take::

  git co -b hannosch/82-frontpage

Edit the any config files you need to get new software (if any) and run::

  bin/buildout

You are now working on your own branch and can pull in additional dependencies
if you want to. Push the branch to Github for other people to see it::

  g push -u

You only need to specify the `-u` the first time, to associate your local
branch with the remote one. Other people will fork your branch and create their
own. If you are working on a larger Epic consisting of multiple stories, use
a branch with the prefix `shared` instead of your username to signal the nature
of it.

After the ticket is done, all tests are written, it's been tested TTW,
upgrade notes or automatic steps are in place and quality assurance has been
performed, you can merge your changes back to master.


Working with CSS
----------------

We are using `SASS <http://sass-lang.com/>`_ to generate our CSS files. On Mac
OS use macports to install it::

  sudo port install rb19-haml

The Ruby 1.8 version available via `rb-haml` is too outdated for our purposes.

To update all CSS files from their SCSS source files, call::

  sass --update src/intranett.theme/intranett/theme/skins/intranett_theme_styles:src/intranett.theme/intranett/theme/skins/intranett_theme_styles


I18N
----

To update the translation files, do::

  sh src/intranett.policy/intranett/policy/rebuild.sh
  sh src/intranett.policy/intranett/policy/sync.sh
