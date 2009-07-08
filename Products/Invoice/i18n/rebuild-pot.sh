#!/bin/bash

#set -x

I18NDOMAIN=Invoice
POT=$I18NDOMAIN.pot-new
LOG=rebuild-pot.log
PYTHON=/usr/bin/python
PWD=`pwd`
PRODUCT=`dirname $PWD`

I18NDUDE=$PRODUCT/../i18ndude/i18ndude
if [ ! -e $I18NDUDE ]; then
    echo "Unable to locate i18ndude utility!"
    exit 1
fi

EXCLUDE_FILES=".svn"
TEMPLATES=`(find $PRODUCT/skins -name '*.*pt') | grep -v $EXCLUDE_FILES`

echo -e "\nRebuilding to $POT - this takes a while, logging to $LOG"

# Using --merge the resulting file is kept sorted by msgid
$PYTHON $I18NDUDE rebuild-pot --pot $POT --create $I18NDOMAIN -s $TEMPLATES >$LOG 2>&1

# Remove '## X more:' occurences
sed -ri "/## [0-9]+ more:/d" $POT

# Made paths relative to Product skins dir
sed -ri "s,$PRODUCT/skins,\.,g" $POT

echo -e "\nTemplates with unneeded literal msgid:\n"
grep 'Unneeded literal msgid in' $LOG | sed -s 's,Unneeded literal msgid in,,' | sort | uniq
echo -e "\nFull report in rebuild-pot.log\n"

exit 0
