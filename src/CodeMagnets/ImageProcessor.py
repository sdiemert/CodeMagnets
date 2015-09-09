__author__ = 'sdiemert'

import pprint
import thread
import threading
from os import listdir

from ShapeFinder import ShapeFinder
from ColorKnnClassifier import ColorKnnClassifier
from LetterKnnClassifier import LetterKnnClassifier
import constants as const
import colorConstants as cc

pp = pprint.PrettyPrinter(indent=4)


class WorkerThread(threading.Thread):

    def __init__(self, row, col, sec, processor):
        threading.Thread.__init__(self)
        self.row = row
        self.col = col
        self.sec = sec
        self.processor = processor

    def run(self):
        r = self.processor.knn.testFromImage(self.sec, show=False, seed=7)
        print int(r[0]), cc.getColorFromNumber(r[0]),
        v = self.processor.ratioKnns[int(r[0])].testFromImage(self.sec, show=False, seed=5)
        x = const.getStringFromNumber(v[0])
        print x, self.row, self.col
        self.processor.lineLocks[self.row].acquire()
        self.processor.output[self.row][self.col] = x
        self.processor.lineLocks[self.row].release()

class CodeMagnetsImageProcessor:
    def __init__(self):
        self.output = []
        self.lineCount = 0
        self.colCount = 0
        self.threads = []
        self.lineLocks = None

    def train(self, readFromFile=True, path="./training3/"):
        """
        train the image processor
        :return: True if the training succeeds, false otherwise.
        """
        self.knn = ColorKnnClassifier()
        self.ratioKnns = []

        for i in range(7):
            self.ratioKnns.append(LetterKnnClassifier())

        if readFromFile:
            f = open(path, 'r')

            for l in f:
                l = l.split(",")
                x = [float(i) for i in l[1:]]
                self.ratioKnns[cc.getColorFromId(int(l[0]))].train.append((int(l[0]), x))

            f.close()

            f = open("color_data.csv", 'r')

            for l in f:
                l = l.split(',')
                x = [float(i) for i in l[1:]]
                self.knn.train.append((int(l[0]), x))

            f.close()

        else:
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
                    self.ratioKnns[c2].loadTrainingImage(path + f, c1)
                    print "LetterClass. " + str(c2) + ":" + str(
                        cc.getColorFromNumber(c2)) + " trained: " + f + " as " + str(const.getStringFromNumber(c1))

        self.knn.trainModel()

        for r in self.ratioKnns:
            r.trainModel()

        print "Completed training"
        print "------------------"

    def process(self, path):

        print "Starting Image Processing"

        sf = ShapeFinder()
        c = sf.getShapeCoordinates(path, show=False)
        lines = sf.getShapesByLines(c)

        self.output = [[] for i in range(len(lines))]
        self.lineLocks = [threading.Lock() for i in range(len(lines))]

        self.lineCount = 0
        self.threads = []

        for l in lines:
            self.colCount = 0
            for s in l:
                z = sf.getSection(s, color=True)
                if z is not None:
                    self.output[self.lineCount].append('')
                    t = WorkerThread(self.lineCount, self.colCount, z, self)
                    t.start()
                    self.threads.append(t)
                    self.colCount += 1

            print ""
            self.lineCount += 1

        for t in self.threads:
            t.join()

        print "Done Image Processing"
        print "---------------------"

        return self.output
