from os import listdir

import numpy as np
import cv2

import constants as const
from KnnClassifier import KnnClassifier
import colorConstants as cc

SEGMENTS = 12


class LetterKnnClassifier(KnnClassifier):
    def __init__(self):
        self.train = [];
        self.knn = cv2.KNearest()

    def populateData(self):

        path = "./training3/"

        fs = listdir(path)

        for f in fs:
            s = f.split(".")
            if len(s) < 2:
                continue

            s = f.split("_")
            if len(s) < 2:
                continue

            c = const.getConstantFromString(s[0])

            c = cc.getColorFromId(c)

            if c is not None:
                self.loadTrainingImage(path + f, c)
                print "trained: " + path + f + " as " + str(c)

        return

    def addTrainingData(self, vals, truth):
        x = self.getData(vals)
        self.train.append((truth, x))

    def loadTrainingImage(self, path, truth):
        r = cv2.imread(path)

        x = self.getData(r)

        self.train.append((truth, x))

    ## Expects color image
    def classify(self, vals):

        vals = cv2.fastNlMeansDenoisingColored(vals, None, 10, 10, 7, 21)

    def getData(self, vals):

        vals = cv2.fastNlMeansDenoisingColored(vals, None, 10, 10, 7, 21)
        bw = cv2.cvtColor(vals, cv2.COLOR_RGB2GRAY)
        vals = cv2.medianBlur(vals, 13)
        bw = cv2.adaptiveThreshold(bw, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 101, 0)

        s = self.getSideRatio(bw)
        r = self.getRatio(bw)
        u = self.subDivideAndCalc(bw)
        x = r
        x += s
        x += u
        return x

    def getSideRatio(self, vals):
        s = vals.shape
        return [100 * (float(s[0]) / float(s[1]))]

    def getRatio(self, vals, thresh=128):
        s = vals.shape
        s = s[0] * s[1]

        count = 0;

        if s == 0:
            return [0]

        for i in np.nditer(vals):
            if i <= thresh:
                count += 1

        r = float(count) / float(s)
        return [r]

    def subDivideAndCalc(self, vals, seg=SEGMENTS, thresh=128):
        x0, y0 = vals.shape
        xn = x0 / seg
        yn = y0 / seg

        result = []
        for i in range(seg):
            tmp = vals[i * xn: (i + 1) * xn - 1, i * yn: (i + 1) * yn - 1]
            v = self.getRatio(tmp, thresh=thresh)
            result.append(v[0])

        return result

    def getColorDist(self, image, show=False):
        r = []
        cs = ('b', 'g', 'r')

        for i, col in enumerate(cs):
            hist = cv2.calcHist([image], [i], None, [256], [0, 256])
            r.append(float(np.argmax(hist)))

        return r

    def get_training_data(self):
        return self.train
