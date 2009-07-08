#!/bin/bash

PYTHON=/usr/bin/python
I18NDUDE=../../i18ndude/i18ndude

if [ ! -e $I18NDUDE ]; then
    echo "Unable to locate i18ndude utility!"
    exit 1
fi

for PO in *.po; do
    $PYTHON $I18NDUDE sync --pot Invoice.pot -s $PO
done
