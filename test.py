#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 15 21:06:46 2020

@author: Javier Alejandro Acevedo Barroso
"""

from keyfinder import *
#Spyder cells
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

#%%

test = Keyfinder(tolerance=0.1)

# test.add_evidence('E', verbose = False)
evidence = ['G','F','D#', 'D', 'A#', 'C', 'A']
# notes = ['C','E','A','F','D']

song_name='Keep on Lying'
print(song_name)
test.add_evidence(evidence)



#%%


test = Keyfinder(tolerance=0.1)

# test.add_evidence('E', verbose = False)
evidence = ['A','C','G','D','E']
# notes = ['C','E','A','F','D']
chords = ['Am']

song_name='Obstacle 1'
print(song_name)
test.add_evidence(evidence)
test.add_evidence(chords, is_it_chords=True)




#%%

test = Keyfinder(tolerance=0.1)

# test.add_evidence('E', verbose = False)
evidence = ['E','F#','A','D','B','C#']
# notes = ['C','E','A','F','D']

song_name='Little Dark Age'
print(song_name)
test.add_evidence(evidence)
#%%

test = Keyfinder(tolerance=0.1)

# test.add_evidence('E', verbose = False)
evidence = ['B','C#','D','A','E']
# notes = ['C','E','A','F','D']
chords = ['D']

song_name='My and Michael'
print(song_name)
test.add_evidence(evidence)
test.add_evidence(chords, is_it_chords=True)


#%%
# test.add_evidence('E', verbose = False)
print("")
test = Keyfinder(tolerance=0.1)
evidence = ['A','B','E','F#','G']
# notes = ['C','E','A','F','D']
# chords = ['D']

song_name='The Heimrich Maneuver'
print(song_name)
test.add_evidence(evidence)
# test.add_evidence(chords, is_it_chords=True)s




#%%
# test.add_evidence('E', verbose = False)
print("")
test = Keyfinder(tolerance=0.1, )
evidence = ['Am']
# notes = ['C','E','A','F','D']
# chords = ['D']

song_name='Angie'
print(song_name)
test.add_evidence(evidence)
# test.add_evidence(chords, is_it_chords=True)

#%%
print("-------")
test = Keyfinder(tolerance=0.1, )
evidence = ['G', 'D','E']
# notes = ['C','E','A','F','D']
chords = [ 'F','Dm','G', ]

song_name='I follow you'
print(song_name)
test.add_evidence(evidence)
test.add_evidence(chords, is_it_chords=True)