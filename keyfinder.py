#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 18:37:02 2020

Object-oriented(ish) version. Takes candidate notes and chords and tries to decide the key.
@author: Javier Alejandro Acevedo Barroso
"""


import numpy as np
import matplotlib.pyplot as plt


notes = np.array(["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"])
names = dict(zip([x for x in range(12)], notes.T))
inv_notes = {v: k for k, v in names.items()}

major = np.array([2,2,1,2,2,2,1])
minor = np.array([2,1,2,2,1,2,2])
blues = np.array([3,2,1,1,3,2])

#i = -3
#for interval in minor:
#    print(names[(12+i)%12])
#    i+= interval
    
class Scale:
    """Class to handle abstract scales"""
    def __init__(self, name, symbol, intervals, variations):
        self.intervals = intervals
        self.symbol = symbol
        self.name= name
        self.variations = variations
        
        
notes = np.array(["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"])
names = dict(zip([x for x in range(12)], notes.T))
inv_notes = {v: k for k, v in names.items()}
class Key:
    """Class to handle a candidate key, and all its information"""

    
    def generate_notes(self):
        i = self.inv_notes[self.note]
        scale_notes = [self.chromatic[i]]
        for interval in self.scale.intervals:
            i+=interval
            # print(self.notes[i%12])
            scale_notes.append(self.chromatic[i%12])
        del scale_notes[-1]
        if(self.verbose):
            print("Key notes", scale_notes)
        return scale_notes

    def generate_chords(self):
        i = self.inv_notes[self.note]
        scale_chords = [self.chromatic[i]+self.scale.variations[0]]
        # print(len(self.scale.variations))
        for interval, j in zip(self.scale.intervals[:-1], range(1,len(self.scale.intervals))):
            i+=interval
            # print(j,len(self.scale.variations[j]))
            scale_chords.append(self.chromatic[i%12]+self.scale.variations[j])
        # del scale_chords[-1]
        if(self.verbose):
            print("Key chords:" ,scale_chords)
        return scale_chords

    def __init__(self, note, scale, verbose = None, prior = None):
        if(verbose == None):
            verbose = False
        self.prior = prior
        self.note = note
        self.verbose = verbose
        # if(len(name) == 1 or name[-1] == '#'):
            # self.name=name+scale.symbol
        # else:
            # self.name = name
        if(len(note) > 1 and note[-1] != '#'):
            raise Exception("Note must be written in the sharp Anglophone convention: A E# B C#")
        self.name=note+scale.symbol
        self.scale = scale
        if(self.verbose):
            print(self.note+ " "+ scale.name)
            print(scale.intervals)
        self.chromatic = np.array(["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"])
        self.names = dict(zip([x for x in range(12)], self.chromatic.T))
        self.inv_notes = {v: k for k, v in self.names.items()}
        i = self.inv_notes[self.note]
        self.notes = self.generate_notes()
        self.chords = self.generate_chords()
       


#%%
major = Scale("Major", "", major, variations = ["","m","m","","","m","dim"])
minor = Scale("Minor", "m", minor, variations = ["m","d","","m","m","",""])
doM = Key(note = "A", scale = minor, verbose = False)
#%%
class Keyfinder:
    """Class to handle the program. It initialices with a list of notes
    and possible scales. Then recieves candidate keys and applies bayesian
    inference to find the most likely key."""
    
    def bayes_numerator(self,key_to_compare,list_to_compare,is_it_chord=False):
        multiplier = 1
        # print(key_to_compare.name,list_to_compare)
        if is_it_chord:
            multiplier = 2
        if(key_to_compare.name not in list_to_compare):
            return self.tolerance/self.total_keys
        else:
            return 1/7 * 1/(multiplier*12) +self.tolerance /self.total_keys

    def single_posterior_chords(self, key_to_compare):
        total = 0
        for possib in (self.keys).values():
            # print(possib.name)
            numerator = self.bayes_numerator(key_to_compare, list_to_compare=possib.chords,is_it_chord=True)
            possib.prior = possib.prior * numerator
            total += possib.prior
        for possib in (self.keys).values():
            possib.prior = possib.prior / total
        return 0
    
    def single_posterior_notes(self, key_to_compare):
        total = 0
        for possib in (self.keys).values():
            # print(possib.name)
            
            numerator = self.bayes_numerator(key_to_compare, list_to_compare=possib.notes)
            possib.prior = possib.prior * numerator
            total += possib.prior
        # for possib in (self.keys).values():
            # possib.prior = possib.prior / total
        return 0
 
    def bayes_posterior(self):
        total = 0
        for key in self.evidence['chords']:
            self.single_posterior_chords(key_to_compare = self.keys[key])
        for key in self.evidence['notes']:
            self.single_posterior_notes(key_to_compare=self.keys[key])
        for key in (self.keys).values():
            total += key.prior
        for key in (self.keys).values():
            key.prior /= total
        return 0


    #Returns the best candidate and prints the others
    def candidates(self, N = 5, verbose = True):
        # posteriors = bayes_posterior(observations=observations, scales=scales,scale_names=candidate_names)
        self.bayes_posterior()
        posteriors = sorted(self.keys.values(), key=lambda x: -x.prior)
        in_best = posteriors[:N]
        # in_best = (-posteriors).argsort()[:N]
        if verbose:            
            print('Key, prob')
            for candidate in in_best:
                print(candidate.name +" {:.3}%".format(candidate.prior*100))
        return in_best[0]
        
    #Adds the new evidence to the old evidence.
    def add_evidence(self,new_evidence, is_it_chords = None, verbose = True):
        if(type(new_evidence)==str):
            new_evidence = [new_evidence]
        if(is_it_chords==None):
            is_it_chords =False
        for name in new_evidence:
            if name[-1] == 'm':
                is_it_chords = True
                break
        
        type_of_evidence = 'notes'
        if is_it_chords:
            type_of_evidence = 'chords'
        for name in new_evidence:
            if len(self.evidence[type_of_evidence]) > 0 and name in self.evidence[type_of_evidence]:
                continue
            else:
                # print(name)
                self.evidence[type_of_evidence].append(name)
        print('Evidence', self.evidence)
        self.candidates(N=8, verbose = verbose)
    

    def __init__(self, notes=None, scales=None, evidence=None, tolerance= 0.01):
        if notes == None:
            notes = np.array(["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"])
        if scales == None:
            major = Scale("Major", "", np.array([2,2,1,2,2,2,1]), variations = ["","m","m","","","m","dim"])
            minor = Scale("Minor", "m", np.array([2,1,2,2,1,2,2]), variations = ["m","dim","","m","m","",""])
            scales = [major, 
                      minor]
        self.notes = notes
        self.scales = scales
        self.scales_dict = {'':self.scales[0], 'm' : self.scales[1], ' ' : self.scales[0]}
        
        # if evidence == None:
        self.evidence = {'chords' : [], 'notes' : []}
        # else:
            # self.evidence = evidence
        self.tolerance = tolerance
        self.total_keys = len(notes) * len(scales)
        keys = [Key(note, scal,prior=1./self.total_keys) for note in notes for scal in scales]
        # chromatic = np.array(["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"])
        self.keys = {}
        for new_key in keys:
            self.keys[new_key.name] = new_key
        if evidence != None:
            self.add_evidence(evidence,is_it_chords=False,verbose = True)
        # self.add_evidence(['Cm'],is_it_chords=False)
        # print(self.keys[0].prior)
        
        
   
