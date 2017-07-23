import cv2
import os
from skimage.measure import compare_ssim as ssim
import matplotlib.pyplot as plt
import numpy as np


imgarrO=[] #images in directory O
imgarrX=[] #images in directory X

#load images
for file in os.listdir("./O"):
    if file.endswith(".png"):
        imgarrO.append(file)

for file in os.listdir("./X"):
    if file.endswith(".png"):
        imgarrX.append(file)

#print(imgarrX)

#test image which compare with images in directory O
testImgFile='test.png'
testImgBW = cv2.imread(testImgFile,cv2.CV_LOAD_IMAGE_GRAYSCALE)
testImg = cv2.imread(testImgFile)

#temp code
"""
while(True):
    cv2.imshow(testImgFile,testImg)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
"""

combinedImgAndSsim={}
combinedImgs=[]
#compare similarity between test image and file in O dir
for fname in imgarrX:
    oImgBW = cv2.imread("./X/"+fname,cv2.CV_LOAD_IMAGE_GRAYSCALE)
    oImg = cv2.imread("./X/"+fname)
    sim = -ssim(testImgBW, oImgBW).__float__()  #similarity function
    combinedImg = cv2.addWeighted(oImg, 0.5,testImg , 0.5, 0)   #combine two graph
    combinedImgAndSsim[sim]=combinedImg

#sort graph imgage
simList=combinedImgAndSsim.keys()
simList.sort()
print (simList)
for sim in simList:
    cv2.imwrite("./SIM/" + (-sim).__str__()[0:5] + ".png", combinedImgAndSsim[sim])
