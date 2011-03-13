context.REQUEST.RESPONSE.setHeader('content-type', 'text/plain; charset=utf-8')

print DateTime()

rates = {'USD':5.44
        ,'EUR':7.98
        ,'UKP':10.86}

print "Conversion rates"
for k,v in rates.items():
    print k,v

query = {}

query['portal_type'] = 'Invoice'

res = context.portal_catalog.searchResults(**query)
print "Found %s invoices" % len(res)

result = []
for i in res:
    r = i.getObject()
    invoicenumber = int(r.getInvoiceNumber())
    if start is not None and invoicenumber < start:
        continue
    if end is not None and invoicenumber > end:
        continue
    result.append((invoicenumber, r))

result.sort()

month = None
total = {}
subtotal = {}

for i in result:
    r = i[-1]
    imonth = r.getInvoiceDate()
    if imonth is not None:
        imonth = imonth.strftime('%Y%m')

        if imonth != month:
            # print and reset subtotal
            print ', '.join(['%s: %s'%(c,v) for c,v in subtotal.items()])
            subtotal = {}

            print ' '
            print r.getInvoiceDate().Month(), r.getInvoiceDate().year()
            month = imonth
    amount = r.getTotal()
    currency = r.getCurrency()
    conversion = rates.get(currency, None)
    if conversion is not None:
        try:
            amount = float(amount) * conversion
            currency = 'NOK'
        except ValueError:
            pass
    if isinstance(amount, (int, float)):
        print r.getInvoiceNumber(), currency, '% 9d' % amount, r.Title()
        # Add to total
        tot = total.get(currency, 0)
        tot += amount
        total[currency] = tot
        stot = subtotal.get(currency, 0)
        stot += amount
        subtotal[currency] = stot
    else:
        print r.getInvoiceNumber(), currency, amount, '!'

print ', '.join(['%s: %s'%(c,v) for c,v in subtotal.items()])
print '\n'
print ', '.join(['%s: %s'%(c,v) for c,v in total.items()])

return printed
