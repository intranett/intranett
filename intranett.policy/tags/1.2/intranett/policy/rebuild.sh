#!/usr/bin/env bash
bin/i18ndude rebuild-pot --pot src/intranett.policy/intranett/policy/locales/intranett.pot --create "intranett" --merge src/intranett.policy/intranett/policy/locales/intranett-manual.pot src/intranett*
bin/i18ndude rebuild-pot --pot src/intranett.policy/intranett/policy/locales/plone.pot --create "plone" --merge src/intranett.policy/intranett/policy/locales/plone-manual.pot src/intranett.policy/intranett/policy/profiles/ src/intranett.theme/intranett/theme/profiles
