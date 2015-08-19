from ShapeFinder import ShapeFinder
from ColorKnnClassifier import ColorKnnClassifier
from LetterKnnClassifier import LetterKnnClassifier
import numpy as np
import constants as const
import colorConstants as cc

import matplotlib.pyplot as plt
import sys
import pprint
import colorConstants as cc
from os import listdir

pp = pprint.PrettyPrinter(indent=4)

print "Starting..."

test_files = ["./training3/example-4-2.jpg"]

knn = ColorKnnClassifier()

ratioKnns = []

for i in range(7):
    ratioKnns.append(LetterKnnClassifier())

print ratioKnns


path = "./training3/"

fs = listdir(path)

for f in fs:
    s = f.split(".")
    if len(s) < 2:
        continue

    s = f.split("_")
    if len(s) < 2:
        continue

    c1 = const.getConstantFromString(s[0])

    c2 = cc.getColorFromId(c1)

    if c2 is not None:
        ratioKnns[c2].loadTrainingImage(path+f, c1)
        print "LetterClass. "+str(c2)+":"+str(cc.getColorFromNumber(c2))+" trained: "+f+ " as "+str(const.getStringFromNumber(c1))

knn.populateData()
knn.trainModel()

for r in ratioKnns:
    r.trainModel()

print "done training"

print len(knn.train)

print [len(r.train) for r in ratioKnns]

print "starting test:"

total_used = 0
total_sum = 0 


for t in test_files:

    sf = ShapeFinder()
    c = sf.getShapeCoordinates(t, show=False)
    lines = sf.getShapesByLines(c)

    for l in lines:
        for s in l:
            z = sf.getSection(s, color=True)
            if z is not None:
                r = knn.testFromImage(z, show=False, seed=7)

                print int(r[0]), cc.getColorFromNumber(r[0]),
                
                v = ratioKnns[int(r[0])].testFromImage(z, show=False, seed=5)

                print const.getStringFromNumber(v[0]) 

        print ""
  
print "Done..."
