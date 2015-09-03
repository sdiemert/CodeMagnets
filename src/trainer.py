__author__ = 'sdiemert'

from os import listdir

from ColorKnnClassifier import ColorKnnClassifier
from LetterKnnClassifier import LetterKnnClassifier
from src.CodeMagnets import constants as const
import src.CodeMagnets.colorConstants as cc

knn = ColorKnnClassifier()
ratioKnns = []


def train(readFromFile=True, path="./training3/"):
    """
    train the image processor
    :return: True if the training succeeds, false otherwise.
    """

    for i in range(7):
        ratioKnns.append(LetterKnnClassifier())

    print ratioKnns

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
            ratioKnns[c2].loadTrainingImage(path + f, c1)
            print "LetterClass. " + str(c2) + ":" + str(
                cc.getColorFromNumber(c2)) + " trained: " + f + " as " + str(const.getStringFromNumber(c1))

    knn.populateData()
    knn.trainModel()

    for r in ratioKnns:
        r.trainModel()

    print "Completed training"
    print "------------------"


if __name__ == "__main__":

    train()

    f = open("data.csv", 'w')
    s = ""
    print "saving to file...."
    print "------------------"
    for r in ratioKnns:
        x = r.get_training_data()
        for val, l in x:
            print val, l
            s = str(val)+","
            count = 0
            for i in l:
                if count >= len(l) - 1:
                    s += str(i)
                else:
                    s += str(i)+","
                count += 1

            f.write(s + "\n")
    f.close()

    f = open("color_data.csv", 'w')

    d = knn.get_training_data()

    for v,l in d:
        s = str(v) + ","
        for i in range(3):
            if i < 2:
                s += str(l[i])+","
            else:
                s += str(l[i])

        print s
        f.write(s+"\n")

    f.close()
