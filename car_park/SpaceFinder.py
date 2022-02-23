import cv2
import pickle

img = cv2.imread('SS.jpg')
width, height= 40,93

try:
    with open("positions",'rb') as f:
        posList=pickle.load(f)

except:
    posList=[]

def mouseClick(events,x,y,flags,params):
    if events == cv2.EVENT_LBUTTONDOWN:
        posList.append((x,y))
    if events == cv2.EVENT_RBUTTONDOWN:
        for i,pos in enumerate(posList):
            x1,y1=pos
            if x1<x<x1+width and y1<y<y1+height:
                posList.pop(i)
    with open("positions",'wb') as f:
        pickle.dump(posList,f)


while True:
    img = cv2.imread('SS.jpg')
    for pos in posList :
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), (255, 0, 255), 2)
    #cv2.rectangle(img,(275,230),(235,323),(255,0,255),2)
    cv2.imshow("screenShot",img)
    cv2.setMouseCallback("screenShot",mouseClick)
    cv2.waitKey(1)


