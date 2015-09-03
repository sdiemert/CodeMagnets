from os import listdir

import numpy as np
import cv2

import constants as const

SEGMENTS = 25


class KnnClassifier:
    def __init__(self):
        self.train = [];
        self.knn = cv2.KNearest()

    def get_training_data(self):
        return self.train

    def populateData(self):

        path = "./training2/"

        fs = listdir(path)

        for f in fs:
            s = f.split(".")
            if len(s) < 2:
                continue

            s = f.split("_")
            if len(s) < 2:
                continue

            c = const.getConstantFromString(s[0])

            if c is not None:
                self.loadTrainingImage(path + f, c)
                print "trained: " + path + f + " as " + str(c)

        return

    def loadTrainingImage(self, path, truth):
        r = cv2.cvtColor(cv2.imread(path), cv2.COLOR_BGR2GRAY)

        x = self.getData(r, invert=True)

        self.train.append((truth, x))

    def getData(self, vals, invert=True):
        if invert:
            vals = cv2.medianBlur(vals, 7)
            vals = cv2.adaptiveThreshold(vals, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 45, 0)
        t = 128
        x = self.getRatio(vals, thresh=t)
        x += self.subDivideAndCalc(vals, thresh=t)
        return x

    def getRatio(self, vals, thresh=80):
        s = vals.shape
        s = s[0] * s[1]
        count = 0

        for i in np.nditer(vals):
            if i <= thresh:
                count += 1

        r = float(count) / float(s)

        return [r]

    def computeThresh(self, vals, sigmas=5):

        std = np.std(vals)
        m = np.mean(vals)

        return m - sigmas * std

    def subDivideAndCalc(self, vals, seg=SEGMENTS, thresh=80):

        x0, y0 = vals.shape

        xn = x0 / seg
        yn = y0 / seg

        result = []
        for i in range(seg):
            tmp = vals[i * xn: (i + 1) * xn - 1, i * yn: (i + 1) * yn - 1]
            v = self.getRatio(tmp, thresh=thresh)
            result.append(v[0])

        return result

    def getHist(self, vals):
        return cv2.calcHist([vals], [0], None, [256], [0, 256])

    def trainModel(self):
        data = []
        labels = []
        for i, j in self.train:
            labels.append(i)
            data.append(j)

        x = np.array(data, np.float32)

        self.knn.train(x, np.array(labels, np.int32))

    def testFromFile(self, path):
        x = self.getRatio(cv2.cvtColor(cv2.imread(path), cv2.COLOR_BGR2GRAY))
        ret, result, a, b = self.knn.find_nearest(np.array([x], np.float32), k=1)
        return ret

    def testFromImage(self, img, show=False, seed=5):
        x = self.getData(img)
        ret, result, a, b = self.knn.find_nearest(np.array([x], np.float32), k=seed)
        return ret, result, a, b


if __name__ == "__main__":
    print "-----------------------start"

    k = KnnClassifier()
    k.populateData()
    k.trainModel()

    x = k.testFromFile("training/plus_1.jpg")

    print "-----------------------done"
