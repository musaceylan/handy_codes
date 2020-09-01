import numpy as np
import cv2 as cv

capture = cv.VideoCapture(0)
lastNorm = 0.0
lastCounter = 0
counter = 0
currentState = 0

onList = []
offList = []

onDuration = 0
offDuration = 0

if not capture.isOpened():
    print("Cannot open camera")
    exit()


while True:
    # Capture frame-by-frame
    ret, frame = capture.read()

    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    hsv = cv.cvtColor(frame,cv.COLOR_BGR2HSV)

    currentNorm = np.linalg.norm(frame)
    diffNorm = currentNorm - lastNorm

    #print("currentNorm " ,currentNorm)
    #print("diffNorm " ,diffNorm)


    if (diffNorm > 20000 and currentState == 0):
        currentState = 1;
    
        print( "on  - was off for " , (counter - lastCounter ), " frames and " , ((counter - lastCounter)/30) ," seconds" )
        offDuration = (counter - lastCounter)/30
        offList.append(offDuration)
        #for v in offList:
        #    print(v + " ")
        lastCounter = counter
        
    if (diffNorm < -20000 and currentState == 1):

        currentState = 0
        print("off - was on  for " ,counter - lastCounter , " frames and " , (counter - lastCounter)/30 , " seconds" )
        onDuration = (counter - lastCounter)/30
        onList.append(onDuration)
        #for v in onList:
        #    print( v + " " )
        lastCounter = counter

    lastNorm = currentNorm
    counter += 1    
    # Display the resulting frame
    cv.imshow('frame', gray)
    if cv.waitKey(1) == ord('q'):
        break


# When everything done, release the capture
capture.release()
cv.destroyAllWindows()


