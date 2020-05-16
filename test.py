#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 15 21:06:46 2020

@author: Javier Alejandro Acevedo Barroso
"""

from keyfinder import *
#%%

test = Keyfinder(tolerance=0.1)

# test.add_evidence('E', verbose = False)
chords = ['Fm','G', 'C#','D#']
# notes = ['C','E','A','F','D']

song_name='Ready to let go'
print(song_name)
test.add_evidence(chords)
# test.add_evidence(notes)
# test.add_evidence(chords)