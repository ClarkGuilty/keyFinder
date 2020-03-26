#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 18:37:02 2020

@author: Javier Alejandro Acevedo Barroso
"""


import numpy as np
import matplotlib.pyplot as plt


notes = np.array(["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"])
names = dict(zip([x for x in range(12)], notes.T))
inv_notes = {v: k for k, v in names.items()}

major = np.array([2,2,1,2,2,2,1])
minor = np.array([2,1,2,2,1,2,2])

i = -3
#for interval in minor:
#    print(names[(12+i)%12])
#    i+= interval
    
    

def generate_scales(notes=notes, scales=[major, minor], s_names = ['', 'm']):
    if(type(notes) != np.ndarray):
        notes = np.array([notes])
    if(type(scales) != list):
        scales = [scales]
    if(type(s_names) != list):
        s_names = [s_names]
    all_scales = {}
    for key in range(12):
        for intervals, name in zip(scales,s_names):
            i = key
            scale = [notes[key]]
            for interval in intervals:
                i+=interval
                scale.append(notes[i%12])
            all_scales[notes[key]+name] = scale
    return all_scales
    

#Se definen las escalas a usar. 
try:
    all_scales
except NameError:
    minor_scales = generate_scales(scales=[minor],s_names=['m'])
    major_scales = generate_scales(scales=[major],s_names=[''])
    all_scales = {**major_scales, **minor_scales}


prior = np.ones(len(all_scales)) / len(all_scales)
prior_names = [x+y for x in notes for y in ['', 'm']]
major_names = [x for x in notes]
minor_names = [x+"m" for x in notes]
priors = dict(zip(prior_names, prior.T))
# print(prior)


    
def bayes_numerator(note, scale,prior = prior):
    if(note not in scale):
        return 0.04/len(prior)
    else:
        return 1/7 * 1/12 +0.04 /len(prior)
    
    
def single_posterior(observation, prior=prior, scales = all_scales, scale_names = prior_names):
    numerators = np.zeros_like(prior)
    for possib, i in zip(scale_names,range(len(scale_names))):
        numerators[i] = bayes_numerator(observation,scales[scale_names[i]], prior=prior)
    posterior = prior * numerators
    posterior = posterior / posterior.sum()
    return posterior
        

# print(single_posterior('C'))

def bayes_posterior(observations, scales=all_scales, scale_names = prior_names):
    if(type(observations) != list):
        observations = np.array([observations])
    posterior = np.ones(len(scales)) / len(scales)
    for observation in observations:
        posterior = single_posterior(observation,prior=posterior,scales=scales, scale_names=scale_names)
    
    return posterior



# print(test)

def candidates(observations, scales = all_scales, candidate_names = prior_names, N = 5):
    posteriors = bayes_posterior(observations=observations, scales=scales,scale_names=candidate_names)
    in_best = (-posteriors).argsort()[:N]
    for candidate in in_best:
        print(prior_names[candidate]+" {:.3}%".format(posteriors[candidate]*100))
    return in_best


test = [ "F","G","D#","C#"]
# test = ["C", "D", "E", "A","B", "F","G"]
print(candidates(test,N=9,scales=major_scales,candidate_names=major_names))










    
    
    
    
    
    
    
    
    
    
    
    
    