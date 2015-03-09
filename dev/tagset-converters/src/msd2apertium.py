# !coding=utf-8
'''
    Skripta koja učitava MSD tag i konvertira ga u CGPOS-ov tagset
    (Ili takvo nešto, sigurno sadrži funkcije koje to rade)
'''

import sys, logging
from msd2apertium_lib import *

if len(sys.argv) != 2:
    # Help printout, if the number of args is invalid
    print ('Usage:')
    print ('\tpython '+sys.argv[0]+' MSD_Tag\t<- convert the msd tag to Apertiumish tag')
    print ('\tpython '+sys.argv[0]+' -c\t<- launch the "console"')
    print
    print ('Example:')
    print ('\tpython ' + sys.argv[0] + ' Afpfpdn')
    print
    sys.exit()
elif len(sys.argv)==2 and sys.argv[1]=='-c':
    # If we provided the '-c' switch, means we're launching the 'console'
    while(True):
        tag=raw_input('MSD-Tag:>')
        print msd2apertium(tag)
else:
    # The 'normal' case, we just convert the tag into apertium's tag format
    print listToTags(msd2apertium(sys.argv[1]))

