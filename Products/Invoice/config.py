from Products.Archetypes.public import DisplayList

PROJECTNAME = 'Invoice'

GLOBALS = globals()

PAYMENT_DUE_OPTIONS = DisplayList((
    (0,  'Immediately'),
    (7,  '1 week'),
    (14, '2 weeks'),
    (21, '3 weeks'),
    (28, '4 weeks'),
    (30, '30 days'),
    (42, '6 weeks')
 ))

DEFAULT_FROM_COMPANY = 'Jarn AS'

DEFAULT_FROM_COMPANY_ADRESS = """
Postboks 2236\nNO-3103 Tønsberg\nNorway\n
"""

DEFAULT_VAT_NUMBER = "986 102 302 MVA"

DEFAULT_PAYMENT_DETAILS = """
Account: 16381456211, Union Bank of Norway\nSWIFT: DNBANOKKXXX\nIBAN : NO73 1638 1456 211\n\n
"""

DEFAULT_NOTE_TEXT = """"""
