#!/usr/bin/env python
# -*- coding: utf-8 -*-

# From original pykey.py
# pykey -- a Python version of crikey,
# http://shallowsky.com/software/crikey
# Simulate keypresses under X11.
#
# This software is copyright 2008 by Akkana Peck.
# Please share and re-use this under the terms of the GPLv2
# or, at your option, any later GPL version.



#############################################################################
# Copyright (C) Labomedia 2014
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franproplin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
#############################################################################
#
# Classe Clavier pour être utilisé dans d'autres scripts
# par exemple We Make Poem

import subprocess
import unicodedata

try:
    import Xlib.display
except ImportError:
    print("You must install python-xlib")
    print("sudo apt-get install python-xlib")
    subprocess.call('sudo apt-get install python-xlib', shell=True)

import Xlib.display
import Xlib.X
import Xlib.XK
import Xlib.protocol.event
import Xlib.ext.xtest

keys_FR = {
    u'0': ("0", 1),
    u'1': ("1", 1),
    u'2': ("2", 1),
    u'3': ("3", 1),
    u'4': ("4", 1),
    u'5': ("5", 1),
    u'6': ("6", 1),
    u'7': ("7", 1),
    u'8': ("8", 1),
    u'9': ("9", 1),
    u'é': ("eacute", 0),
    u'è': ("egrave", 0),
    u'ù': ("ugrave", 0),
    u'à': ("agrave", 0),
    u'ê': ("ecircumflex", 3),
    u'â': ("acircumflex", 3),
    u'ô': ("ocircumflex", 3),
    u'î': ("icircumflex", 3),
    u'û': ("ucircumflex", 3),
    u'ï': ("idiaeresis", 4),
    u'ü': ("udiaeresis", 4),
    u'ë': ("ediaeresis", 4),
    u'ä': ("adiaeresis", 4),
    u'ö': ("odiaeresis", 4),
    u'ç': ("ccedilla", 0),
    u'É': ("eacute", 5),
    u'À': ("agrave", 5),
    u'Ô': ("ocircumflex", 6),
    u'Û': ("ucircumflex", 6)
    }

special_X_keysymbols = {
    u' ': ("space", 0),
    u'\t': ("Tab", 0),
    u'\n': ("Return", 0),  # for some reason this needs to be cr, 0), not lf
    u'\r': ("Return", 0),
    u'\e': ("Escape", 0),
    u'!': ("exclam", 0),
    u'#': ("numbersign", 2),
    u'%': ("percent", 1),
    u'$': ("dollar", 0),
    u'&': ("ampersand", 0),
    u'"': ("quotedbl", 0),
    u'\'': ("apostrophe", 2),
    u'(': ("parenleft", 0),
    u')': ("parenright", 0),
    u'*': ("asterisk", 0),
    u'=': ("equal", 0),
    u'+': ("plus", 1),
    u',': ("comma", 0),
    u'-': ("minus", 0),
    u'.': ("period", 1),
    u'/': ("slash", 1),
    u':': ("colon", 0),
    u';': ("semicolon", 0),
    u'<': ("less", 0),
    u'>': ("greater", 1),
    u'?': ("question", 1),
    u'@': ("at", 2),
    u'[': ("bracketleft", 2),
    u']': ("bracketright", 2),
    u'\\': ("backslash", 0),
    u'^': ("asciicircum", 2),
    u'_': ("underscore", 0),
    u'`': ("grave", 2),
    u"'": ("acute", 0),
    u'{': ("braceleft", 2),
    u'|': ("bar", 2),
    u'}': ("braceright", 2),
    u'~': ("asciitilde", 2),
    u'£': ('sterling',1),
    u'§': ('paragraph',1),
    u'µ': ('mu',1)
    }


class without_copy_past(object):
    '''Simule une saisie clavier à partir d'un caractère en unicode.'''
    def __init__(self, Keyboard="FR"):
        '''Dans un terminal, 'xev' pour récupèrer les keycode ou les keysym.'''
        self.display = Xlib.display.Display()
        self.window = self.display.get_input_focus()._data["focus"]
        self.spe_keysymb = special_X_keysymbols
        if Keyboard == "FR":
            self.keys_FR = keys_FR
        self.Maj = self.keysym_2_keycode(0xffe1) # 50
        self.Altgr = self.keysym_2_keycode(0xfe03) # 108
        self.Circonflex = self.keysym_2_keycode(0xfe52) # 34

    def get_caract_type(self, caract):
        '''Upper, special or Frenchie ?'''
        key_type = "lower"
        if caract.isupper():
            key_type = "upper"
        for spk in self.spe_keysymb.keys():
            if caract == spk:
                key_type = "special"
        for kfr in self.keys_FR.keys():
            if caract == kfr:
                key_type = "FR"
        return key_type

    def get_keysym(self, caract):
        '''Retourne le keysymbol du caractère.'''
        keysym = Xlib.XK.string_to_keysym(caract)
        return keysym

    def keysym_2_keycode(self, keysym):
        '''Retourne le keycode du keysymbol.'''
        keycode = self.display.keysym_to_keycode(keysym)
        return keycode

    def get_keycode(self, caract):
        '''Retourne la simulation du caractère sous linux.
        Unfortunately, although this works to get the correct keysym
        i.e. keysym for '#' is returned as "numbersign"
        the subsequent display.keysym_to_keycode("numbersign") is 0.
        '''
        key_type = self.get_caract_type(caract)
        keysymverif = self.get_keysym(caract)

        if key_type == "lower":
            keysym = self.get_keysym(caract)
            key_comp = 0
        if key_type == "special":
            keysym = self.get_keysym(self.spe_keysymb[caract][0])
            # La touche complémentaire est le 2ème du tuple
            key_comp = self.spe_keysymb[caract][1]
        if key_type == "upper":
            keysym = self.get_keysym(caract)
            key_comp = Xlib.X.ShiftMask
        if key_type == "FR":
            keysym = self.get_keysym(self.keys_FR[caract][0])
            # La touche complémentaire est le 2ème du tuple
            key_comp = self.keys_FR[caract][1]

        keycode = self.keysym_2_keycode(keysym)
        valid = True

        if key_comp == 0:
            comp = "None"
        if key_comp == 1:
            comp = "self.Maj"
        if key_comp == 2:
            comp = "self.Altgr"
        if key_comp == 3:
            comp = "self.Circonflex"
        if key_comp == 4:
            comp = "trema"

        #self.print_control(caract, keycode, keysym, comp, keysymverif)
        if keysym == 0:
            # Caractère non étudié
            print("{0} n'a pas été étudié".format(caract.encode('utf8')))
            valid = False
        return keycode, key_comp, valid

    def print_control(self, caract, keycode, keysym, comp, keysymverif):
        print("\n{0}: soit {1}, touche symbole {2} {4},\
                touche complémentaire {3}".
        format(caract.encode('utf8'), keycode, keysym, comp, keysymverif))

    def simul_unicode(self, caract):
        '''Simulation d'un seul caractactère en unicode.'''
        if isinstance(caract, unicode):
            self.apply_keycode(caract)

    def simul_ascii(self, caract):
        '''Conversion avec perte en ascii'''
        lettre = unicodedata.normalize('NFKD', caract).encode('ascii','ignore')
        lettre = lettre.decode('utf-8')
        self.simul_unicode(lettre)

    def apply_keycode(self, caract):
        '''C'est de l'unicode, j'applique le keycode.'''
        keycode, key_comp, valid = self.get_keycode(caract)

        if valid:
            # Touche simple
            if key_comp == 0:
                self.touche_simple(keycode)
            # self.Majuscule
            if key_comp == 1:
                self.majuscule(keycode)
            # Avec self.Altgr
            if key_comp == 2:
                self.altgr(keycode)
            # Accent self.Circonflex
            if key_comp == 3:
                self.circonflex(keycode)
            # Tréma
            if key_comp == 4:
                self.trema(keycode)
            # Majuscule accentuée simple
            if key_comp == 5:
                self.majuscule_avec_accent(keycode)
            # Majuscule accentuée circonflex
            if key_comp == 6:
                self.majuscule_avec_accent_circonflex(keycode)
            # Actualisation de l'affichage
            self.display.sync()

    def touche_simple(self, keycode):
        # Appui puis relachement de la touche keycode
        self.key_on(keycode)
        self.key_off(keycode)

    def majuscule(self, keycode):
        # Simulation de la touche majuscule enfoncée
        self.key_on(self.Maj)
        # Comme une touche simple
        self.touche_simple(keycode)
        # Relachement de la touche majuscule enfoncée
        self.key_off(self.Maj)

    def altgr(self, keycode):
        # Simulation de la touche Altgr enfoncée 0xfe03
        self.key_on(self.Altgr)
        # Comme une touche simple
        self.touche_simple(keycode)
        # Relachement de la touche Altgr enfoncée
        self.key_off(self.Altgr)

    def circonflex(self, keycode):
        # Comme une touche simple pour circonflex
        self.touche_simple(self.Circonflex)
        # Puis le caractère
        self.touche_simple(keycode)

    def trema(self, keycode):
        # Simulation de la touche majuscule enfoncée
        self.key_on(self.Maj)
        # Comme une touche simple pour tréma en maj
        self.touche_simple(self.Circonflex)
        # Relachement de la touche majuscule enfoncée
        self.key_off(self.Maj)
        # Puis le caractère
        self.touche_simple(keycode)

    def majuscule_avec_accent(self, keycode):
        # Verrouillage majuscule, Caps Lock
        self.touche_simple(66)
        # Touche simple accentuée
        self.touche_simple(keycode)
        # Déverrouillage majuscule
        self.touche_simple(66)

    def majuscule_avec_accent_circonflex(self, keycode):
        # Verrouillage majuscule, Caps Lock
        self.touche_simple(66)
        # Caractère avec circonflex
        self.circonflex(keycode)
        # Déverrouillage majuscule
        self.touche_simple(66)

    def key_on(self, keycode):
        '''Equivaut à appuyer sur key.'''
        Xlib.ext.xtest.fake_input(self.display, Xlib.X.KeyPress, keycode)

    def key_off(self, keycode):
        '''Relache key.'''
        Xlib.ext.xtest.fake_input(self.display, Xlib.X.KeyRelease, keycode)
