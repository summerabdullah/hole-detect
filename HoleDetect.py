
#!/usr/bin/env python
"""Hole Detect Farmware"""

from farmware_tools import device

import cv2
import numpy as np;
im = cv2.imread("blob.jpeg", cv2.IMREAD_GRAYSCALE)
angle = 21.1
scaleFactor = 4.882
holes = []
def rotateAndScale(img, scaleFactor, degreesCCW):
    (oldY,oldX) = img.shape 
    M = cv2.getRotationMatrix2D(center=(oldX/2,oldY/2), angle=degreesCCW, scale=scaleFactor) 

    newX,newY = oldX*scaleFactor,oldY*scaleFactor
    
    r = np.deg2rad(degreesCCW)
    newX,newY = (abs(np.sin(r)*newY) + abs(np.cos(r)*newX),abs(np.sin(r)*newX) + abs(np.cos(r)*newY))
    
    (tx,ty) = ((newX-oldX)/2,(newY-oldY)/2)
    M[0,2] += tx 
    M[1,2] += ty

    rotatedImg = cv2.warpAffine(img, M, dsize=(int(newX),int(newY)))
    return rotatedImg
img = cv2.imread('blob.jpeg',0)
rot = rotateAndScale(img, 1.0, angle)

###########################################################################

params = cv2.SimpleBlobDetector_Params()
params.minThreshold = 40
params.maxThreshold = 120
params.filterByCircularity = True
params.minCircularity = 0.78

params.filterByArea = True
params.minArea = 20

ver = (cv2.__version__).split('.')
if int(ver[0]) < 3 :
	detector = cv2.SimpleBlobDetector(params)
else : 
	detector = cv2.SimpleBlobDetector_create(params)

keypoints = detector.detect(rot)

im_with_keypoints = cv2.drawKeypoints(rot, keypoints, np.array([]), (0,0,250), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

#############################################################################

h, w = rot.shape
print (h/2, w/2)

print (len(keypoints))

for x in range(len(keypoints)):
  
  print(keypoints[x].pt[0] , str(',') ,  keypoints[x].pt[1])      
  holes.append([((w/2)-keypoints[x].pt[0])/scaleFactor,((h/2)-keypoints[x].pt[1])/scaleFactor])           

for x in range(len(holes)):
  print(holes[x])      


cv2.imshow("Keypoints", im_with_keypoints)
cv2.waitKey(0)

