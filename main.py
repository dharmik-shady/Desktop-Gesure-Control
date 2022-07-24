import cv2
import numpy as np
import handmodule as htm
import time
import pyautogui

####################################
# wCam, hCam = pyautogui.size() # For full screen webCam
wCam, hCam = 640, 480
p1, p2 = int((wCam/640)*400), int((hCam/480)*100)
p3, p4 = wCam-int((wCam/640)*100), hCam-int((hCam/480)*280)
smoothening = 9
#####################################

pTime=0
cx1 = 0
cx2 = 0
cx3 = 0
cy1 = 0
cy2 = 0
cy3 = 0
plocX, plocY = 0, 0
clocX, clocY = 0, 0

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
detector = htm.handDetector(maxHands=1)
wScr, hScr = pyautogui.size()

while True:
    # find landmark
    success, img = cap.read()
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img, draw=False)
    # get tip of finger
    if len(lmList) != 0:
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]
        x3, y3 = lmList[16][1:] 
        cx1 = x1
        cx2 = x2
        cx3 = x3
        cy1 = y1
        cy2 = y2
        cy3 = y3    
        # check which finger is up
        fingers = detector.fingersUp()
        cv2.rectangle(img, (p1, p2), (p3, p4), (255, 0, 255), 2)    
        # only index finger: moving mode
        if fingers[1] == 1 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 0 and fingers[0] == 1:
            # convert coordinates
            inx = np.interp(x1, (p1, p3), (0, wScr))
            iny = np.interp(y1, (p2, p4), (0, hScr))
            # smoothening values
            clocX = plocX + (inx-plocX) / smoothening
            clocY = plocY + (iny-plocY) / smoothening   
            # move mouse to x=clocX, y=clocY
            pyautogui.moveTo(x=clocX, y=clocY)
            # autopy.mouse.move(wScr-clocX, clocY)
            cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
            plocX, plocY = clocX, clocY 
        # both index and thumb up: clicking mode
        if fingers[1] == 1 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 0 and fingers[0] == 0:
            # distance between finger
            length, img, lineInfo = detector.findDistance(4, 5, img, draw=False)
            # click if distance short
            if length > 50:
                cv2.circle(img, (x1, y1), 15, (0, 255, 0), cv2.FILLED)
                pyautogui.click(clicks=1, interval=0.3)
        # VOLUME CONTROL
        if fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 0 and fingers[4] == 0 and fingers[0] == 0:

            cv2.putText(img, str("Volume Control"), (200,100), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255), 3)   
            if (cy1+10) < py1 and cy2 < py2:
                pyautogui.press("volumeup")
            if (cy1-10) > py1 and cy2 > py2:
                pyautogui.press("volumedown")


    # frame rate
    cTime = time.time()
    fps = 1/(cTime - pTime)
    # x coordinate
    px1 = cx1
    px2 = cx2
    px3 = cx3
    # y coordinate
    py1 = cy1
    py2 = cy2
    py3 = cy3
    pTime = cTime
    
    cv2.putText(img, str(int(fps)), (10,200), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255), 3)

    cv2.imshow("Image", img)
    key = cv2.waitKey(2)
    if key==ord('q') or key ==ord('Q'):
        break
cap.release()
