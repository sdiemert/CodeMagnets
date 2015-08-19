import numpy as np
import cv2 
import cv2.cv as cv
import matplotlib.pyplot as plt
from math import sqrt
import tesseract

class ShapeFinder: 

    def __init__(self):
        self.contours = None
        self.image = None
        self.original_image = None

    def getShapeCoordinates(self, path, show=False):

        image = cv2.imread(path, 1)

        self.colorImage = np.copy(image)

        #print "image"
        #print image
        #print image.shape

        image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        x = cv2.cvtColor(cv2.imread(path),cv2.COLOR_BGR2GRAY)

        self.original_image = np.copy(image)

        if show:
            plt.imshow(x)
            plt.show()

        """
        print "self.original_image"
        print self.original_image
        print self.original_image.shape
        print '============================'
        """

        image = cv2.medianBlur(image, 7)

        image = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 45, 0)

        self.threshImage = np.copy(image)

        # Perform morphology
        se = np.ones((7,7), dtype='uint8')
        image_close = cv2.morphologyEx(image, cv2.MORPH_CLOSE, se)

        #save the image in the class
        self.image = image

        cnt = cv2.findContours(image_close, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[0]

        self.contours = cnt

        result = []

        for c in cnt:
            result.append((cv2.boundingRect(c)))

        return result

    def getContours(self):
        return self.contours

    def showContours(self): 
        mask = np.zeros(self.image.shape[:2], np.uint8)
        cv2.drawContours(mask, self.contours, -1, 255, -1)
        plt.subplot(1,2,1)
        plt.imshow(mask)
        plt.subplot(1,2,2)
        plt.imshow(self.original_image)
        plt.show()

    def _stat(self, lst):
        """Calculate mean and std deviation from the input list."""
        n = float(len(lst))
        mean = sum(lst) / n
        stdev = sqrt((sum(x*x for x in lst) / n) - (mean * mean)) 
        return mean, stdev

    def _cluster2(self, lst, n, thresh=100):
        result = []
        cluster = []

        for i,t in zip(range(len(lst)), lst):
            if len(cluster) < 1:
                cluster.append(t)
                continue

            mean, std = self._stat([y for x,y,w,h in cluster])

            if std == 0 or len(cluster) == 1:
                if abs(cluster[0][1] - t[1]) < thresh:
                    cluster.append(t)
                else:
                    result.append(cluster)
                    cluster = [t]
            else:
                if abs(t[1] - mean) < std*n :
                    cluster.append(t)
                else:
                    result.append(cluster)
                    cluster = [t]

        if len(cluster) > 0:
            result.append(cluster) 

        return result

    def sortByXCoord(self, a, b):
        if a[0] == b[0]:
            return 0
        elif a[0] < b[0]:
            return -1
        else:
            return 1


    def getShapesByLines(self, shapes):
        '''
        Loop through and find shapes that have similar y coordinates
        '''
        shapes = sorted(shapes, key=lambda student: student[1])            

        r = self._cluster2(shapes, 6)
        rr = []

        for t in r:
            t.sort(self.sortByXCoord)
            rr.append(t)
        return rr

    def getSection(self, shape, color = False):
        #tmp = self.original_image[shape[1]:shape[1]+shape[3],shape[0]:shape[0]+shape[2]]
        if color:
            tmp = self.colorImage[shape[1]:shape[1]+shape[3],shape[0]:shape[0]+shape[2]]
        else:
            tmp = self.threshImage[shape[1]:shape[1]+shape[3],shape[0]:shape[0]+shape[2]]

        r = tmp.shape
        if r[0] * r[1] < 400:
            return None
        else:
            return tmp
