
import cv2
import os
fname="graph.png"
imgfile = cv2.imread(fname)
bgfile=cv2.cvtColor(imgfile,cv2.COLOR_BGR2GRAY)
bgfile=cv2.Laplacian(bgfile,cv2.CV_8UC1)
ret, thresh = cv2.threshold(bgfile, 127, 255, 0)
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
draw=[]
for i in range(0,len(contours)):
    draw.append(imgfile)
for i, c in enumerate(contours):
    cv2.drawContours(draw[i],contours,i,(0,255,0),-1)
while True:
    for i in range(0, len(contours)):
        cv2.imshow(str(i),draw[i])
    cv2.imshow("thresh",thresh)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break