import cv2
import numpy as np
import os
from cvzone.HandTrackingModule import HandDetector as hd

cam = cv2.VideoCapture(0)

cam.set(3, 1280)
cam.set(4, 720)

detector = hd()

folder = 'Presentations'
images = os.listdir(folder)

img_number = 0
ws, hs = 213, 120
threshold = 425

buttonPressed = False
buttonCounter = 0
buttonDelay = 10

annotations = [[]]
annotationsNumber = -1
annotationsFlag = False

while True:
    _, img = cam.read()
    img = cv2.flip(img, 1)

    # images[img_number] = cv2.resize(images[img_number], (1280, 720), interpolation=cv2.INTER_AREA)
    current_image = os.path.join(folder, images[img_number])
    img_current = cv2.imread(current_image)
    img_current = cv2.resize(img_current, (1280, 720), interpolation=cv2.INTER_AREA)

    h, w, _ = img_current.shape

    hands, img = detector.findHands(img)
    lmList = detector.findPosition(img)

    cv2.line(img, (0, threshold), (1280, threshold), (0, 255, 0), 10)

    if hands:
        fingers = detector.fingersUp(hands[0])

    if lmList and not buttonPressed:

        cx, cy = hands[0]['center']

        if cy <= threshold:

            if fingers[0]:
                buttonPressed = True
                img_number = max(0, img_number - 1)
                annotations = [[]]
                annotationsNumber = -1
                annotationsFlag = False

            elif fingers[4]:
                buttonPressed = True
                img_number = min(3, img_number + 1)
                annotations = [[]]
                annotationsNumber = -1
                annotationsFlag = False

        x1, y1 = lmList[8][1], lmList[8][2]
        x1 = int(np.interp(x1, [1280 // 2, w], [0, 1280]))
        y1 = int(np.interp(y1, [150, 720 - 150], [0, 720]))

        if fingers[1] and fingers[2]:
            annotationsFlag = False
            cv2.circle(img_current, (x1, y1), 20, (0, 0, 255), -1)

        if fingers[1] and not fingers[2]:
            if not annotationsFlag:
                annotationsFlag = True
                annotationsNumber += 1
                annotations.append([])
            cv2.circle(img_current, (x1, y1), 20, (0, 0, 255), -1)
            annotations[annotationsNumber].append([x1, y1])
        else:
            annotationsFlag = False

        if fingers == [0, 1, 1, 1, 0]:
            if annotations:
                annotations.pop(-1)
                annotationsNumber -= 1
                buttonPressed = True

    if buttonPressed:
        buttonCounter += 1
        if buttonCounter > buttonDelay:
            buttonCounter = 0
            buttonPressed = False

    for i in range(len(annotations)):
        for j in range(len(annotations[i])):
            if j:
                cv2.line(img_current, annotations[i][j - 1], annotations[i][j], (0, 0, 200), 10)

    img_Small = cv2.resize(img, (ws, hs))
    img_current[:hs, w - ws: w] = img_Small

    cv2.imshow('Presentation', img_current)
    # cv2.imshow('img', img)
    cv2.waitKey(1)

