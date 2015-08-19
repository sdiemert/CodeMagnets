import numpy as np
from matplotlib import pyplot as plt
import cv2
import constants as const
from os import listdir
from os.path import isfile, join

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

        #print fs

        for f in fs:
            s = f.split(".")
            if len(s) < 2:
                continue

            s = f.split("_")
            if len(s) < 2:
                continue

            c = const.getConstantFromString(s[0])

            if c is not None:
                self.loadTrainingImage(path+f, c)
                print "trained: "+path+f+ " as "+str(c)
             
        return 

    def loadTrainingImage(self, path, truth):
        r = cv2.cvtColor(cv2.imread(path),cv2.COLOR_BGR2GRAY)

        x = self.getData(r, invert = True)

        self.train.append((truth, x))

   
    def getData(self, vals, invert = True):
        if invert: 
            vals = cv2.medianBlur(vals, 7)
            vals = cv2.adaptiveThreshold(vals, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 45, 0)
        #plt.imshow(vals)
        #plt.show()
        #t = self.computeThresh(vals, sigmas=3)
        t = 128
        x = self.getRatio(vals, thresh=t)
        x += self.subDivideAndCalc(vals, thresh = t)
        #print "vector: ", x 
        return x

    def getRatio(self, vals, thresh = 80):
        s = vals.shape
        #print "Shape: ", s 
        s = s[0]*s[1]
        #print "Shape Size: ", s 

        count = 0; 

        #thresh = self.computeThresh(vals, 1.2)

        for i in np.nditer(vals):
            if i <= thresh :
                count += 1

        #np.set_printoptions(threshold='nan')
        r = float(count)/float(s)
        #print "count: ", count
        #print "ratio:" , r 
        return [ r ] 
        #np.set_printoptions(threshold=5)

    def computeThresh(self, vals, sigmas = 5): 

        std = np.std(vals) 
        m   = np.mean(vals)

        #print "STD, MEAN, THRESH: ", std, m, m + sigmas*std

        return m - sigmas*std

    def subDivideAndCalc(self, vals, seg=SEGMENTS, thresh = 80):

        x0,y0 = vals.shape

        #print "Input shape: ", vals.shape

        #plt.imshow(vals)
        #plt.show()

        xn = x0/seg
        yn = y0/seg
    

        result = []
        for i in range(seg):
            tmp = vals[i*xn : (i+1)*xn-1, i*yn : (i+1)*yn-1]
            #plt.imshow(tmp)
            #plt.show()
            #print "subDivide tmp.shape: ",tmp.shape
            v = self.getRatio(tmp, thresh=thresh)
            #print "retruned ratio: ", v
            result.append(v[0])

        return result

    def getHist(self, vals):
        return cv2.calcHist([vals],[0], None, [256], [0, 256])

    def trainModel(self):
        data = []
        labels = []
        for i,j in self.train:
            labels.append(i)
            data.append(j)

        x = np.array(data, np.float32)

        self.knn.train(x, np.array(labels, np.int32))

    def testFromFile(self, path):
        x = self.getRatio(cv2.cvtColor(cv2.imread(path),cv2.COLOR_BGR2GRAY))
        #x = [y[0] for y in x]
        ret,result,a,b = self.knn.find_nearest(np.array([x], np.float32), k=1) 
        return ret

    def testFromImage(self, img, show=False, seed = 5):
        if show:
            plt.imshow(img)
            plt.show()
        x = self.getData(img)
        ret,result,a,b = self.knn.find_nearest(np.array([x], np.float32), k=seed) 
        return ret,result, a, b

if __name__ == "__main__":

    print "-----------------------start"

    k = KnnClassifier()
    k.populateData()
    k.trainModel()
    
    x =  k.testFromFile("training/plus_1.jpg")

    print "-----------------------done"
