import sys
import base64
import time
from without_copy_past import without_copy_past

keyboard = without_copy_past(Keyboard="FR")

time.sleep(5)

file = open('text_base64.py','r')

data = file.read()

encoded = base64.b64encode (data)
decode = base64.b64decode(encoded).decode('UTF-8')
encoded += u""
decode += u""

def main():
    for caract in encoded:
        time.sleep(0.005)
        keyboard.simul_unicode(caract)
    for caract in decode:
        time.sleep(0.005)
        keyboard.simul_unicode(caract)
main()
