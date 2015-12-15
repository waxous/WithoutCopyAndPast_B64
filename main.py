import sys
from base64 import b64encode
import time
import argparse
from without_copy_past import without_copy_past

parser = argparse.ArgumentParser(description='Simulate keystroke for transfer file in b64 when no other vector is allowed')
parser.add_argument('-f', type=file, required=True, help='File to transfer')
parser.add_argument('-k', default='FR', choices=['FR'], help='Choose your keyboard (doesn\'t work yet)')
parser.add_argument('-w', type=float, default=5, help='Time before typing begins')
parser.add_argument('-b', type=float, default=0.005, help='Time to wait between each strokes')
parser.add_argument('-s', type=bool, nargs='?', default=False, const=True, help='Don\'t run but estimate time of transfer')

args = parser.parse_args()

keyboard = without_copy_past(Keyboard=args.k)

data = args.f.read()
encoded = unicode(b64encode(data))

if args.s:
    seconds = args.b*len(encoded)
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    print "Encoded size : %.2f kbyte"%(len(encoded)/1000)
    stringTime = ''
    if h != 0:
        stringTime += '%d hours '%h
    if m != 0:
        stringTime += '%d minutes '%m
    if s != 0:
        if len(stringTime) != 0:
            stringTime += 'and '
        stringTime += '%d seconds'%s
    print "Estimated time : %s" % stringTime
    print "Speed : %.2f byte/s"%(1/args.b)
else:
    print "You have %.2f seconds to select the window before I'll start to type"%args.w
    time.sleep(args.w)
    for caract in encoded:
        time.sleep(args.b)
        keyboard.simul_unicode(caract)
