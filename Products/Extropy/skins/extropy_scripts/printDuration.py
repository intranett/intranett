## Script (Python) "roundAndPrintDuration"
##title=Print estimates in a human-readable form
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=hours

from DateTime import DateTime
from math import floor

output = ""

if hours is None:
    return ""
hours = float(hours)

# we do big rounding
# a work week in this equation is roughly 30 hours
x = floor(hours / 30.0)
if x:
    if x == 1:
        output = "a week"
    elif x > 1:
        output = "%s weeks" %(int(x),)
    remain = hours % 30
    if remain >= 6:
        days= round(remain / 6)
        output  +=  " and %s day" %(int(days),)
        if days > 1:
            output += "s"
    return output

# no weeks. days, then
if hours == 0:
    return ""

if hours < 0.75:
    return "less than an hour"

if 0.75 < hours <= 1.1 :
    return "an hour"

if 1.1 < hours <= 2.1:
    return "2 hours"

if 2.1 < hours <= 4.0:
    return "half a day"

if 4.0 < hours <= 7:
    return "a day"

if hours > 7:
    x = hours / 6.0
    remain = hours % 6
    if remain >= 2:
        half = " 1/2"
    else:
        half=""
    return "%s%s days" %(int(x),half)

# then hours
x = hours
if x >= 1:
    output = "%s hours"
