import cv2
import pickle
import cvzone
import numpy as np
width, height= 40,93
cap = cv2.VideoCapture('footage.mp4')
#cap = cv2.VideoCapture(0)
# Read the position from file

with open("positions", 'rb') as f:
    posList = pickle.load(f)

def SpaceFinder(imgPro):

    spaceCounter=0
    for pos in posList:
        x,y=pos

        # crop the images on parking slots
        imgCrop=imgPro[y:y+height,x:x+width]
        # cv2.imshow(str(x*y),imgCrop)

        # get the pixel Counts in cropped image
        count = cv2.countNonZero(imgCrop)

        # uncomment below line to see the pixel count
        # cvzone.putTextRect(img, str(count), (x, y + height - 3), scale=1, thickness=2, offset=0, colorR=(0,0,255))

        # Based on conditions decide the colour and thikness on rectangle and update free space count
        if count < 500:
            spaceCounter += 1
            color = (0,255,0)
            thinkness=5
        else:
            color = (0, 0, 255)
            thinkness=2

        # dependeing upon value colour change of box
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), color, thinkness)

    # printing free space on img
    cvzone.putTextRect(img, f'Free : {spaceCounter}/{len(posList)}', (450,200), scale=1.5, thickness=2, offset=2, colorR=(0,255,0))


while True:

    # loopinf video for nonstop play
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES,0)

    # reading image parameter
    success,img=cap.read()

    # converting img to GRAY
    imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    # converting GRAY to Blur img
    imgBlur = cv2.GaussianBlur(imgGray,(3,3),1)

    # generating threshold values
    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                         cv2.THRESH_BINARY_INV, 25, 16)

    # generating median img
    imgMedian = cv2.medianBlur(imgThreshold, 5)

    # converting in values
    kernel = np.ones((3, 3), np.uint8)

    # generating Dilate img
    imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)

    # sending Dilate img to funtion
    SpaceFinder(imgDilate)
#    cv2.imshow("Image", img)
#    cv2.imshow("ImageBlur", imgBlur)
#    cv2.imshow("ImageThres", imgMedian)
#    for pos in posList :


    # video play
    cv2.imshow('video',img)
    cv2.waitKey(10)

