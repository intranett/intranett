#!/usr/bin/env bash
bin/i18ndude sync --pot src/intranett.policy/intranett/policy/locales/intranett.pot src/intranett.policy/intranett/policy/locales/en/LC_MESSAGES/intranett.po
msgfmt --no-hash -o src/intranett.policy/intranett/policy/locales/en/LC_MESSAGES/intranett.mo src/intranett.policy/intranett/policy/locales/en/LC_MESSAGES/intranett.po
bin/i18ndude sync --pot src/intranett.policy/intranett/policy/locales/plone.pot src/intranett.policy/intranett/policy/locales/en/LC_MESSAGES/plone.po
msgfmt --no-hash -o src/intranett.policy/intranett/policy/locales/en/LC_MESSAGES/plone.mo src/intranett.policy/intranett/policy/locales/en/LC_MESSAGES/plone.po
bin/i18ndude sync --pot src/intranett.policy/intranett/policy/locales/intranett.pot src/intranett.policy/intranett/policy/locales/no/LC_MESSAGES/intranett.po
msgfmt --no-hash -o src/intranett.policy/intranett/policy/locales/no/LC_MESSAGES/intranett.mo src/intranett.policy/intranett/policy/locales/no/LC_MESSAGES/intranett.po
bin/i18ndude sync --pot src/intranett.policy/intranett/policy/locales/plone.pot src/intranett.policy/intranett/policy/locales/no/LC_MESSAGES/plone.po
msgfmt --no-hash -o src/intranett.policy/intranett/policy/locales/no/LC_MESSAGES/plone.mo src/intranett.policy/intranett/policy/locales/no/LC_MESSAGES/plone.po
