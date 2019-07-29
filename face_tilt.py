import imutils
from imutils import face_utils
import numpy as np
import argparse
import imutils
import dlib
import cv2
import collections
from collections import OrderedDict
from statistics import mean
import math
import sys

FACIAL_LANDMARKS_IDXS = OrderedDict([
	('nose', (27, 31))
])

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('detect-face-parts/shape_predictor_68_face_landmarks.dat')

def faceline(pic):
    gradient = []

    image = cv2.imread(pic)
    image = imutils.resize(image, width=500)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    rects = detector(gray, 1)

    if len(rects) > 1:
        return 'recterror'

    vector = []

    for (i, rect) in enumerate(rects):
        shape = predictor(gray, rect)
        shape = face_utils.shape_to_np(shape)

    for (name, (i, j)) in FACIAL_LANDMARKS_IDXS.items():
        clone = image.copy()
        cv2.putText(clone, name, (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
            0.7, (0, 0, 255), 2)

        for (x, y) in shape[i:j]:
            cv2.circle(clone, (x, y), 1, (0, 0, 255), -1)
            temp = {'x' : x, 'y' : y}
            vector.append(temp)

    q = 0
    startx = 0
    starty = 0
    endx = 0
    endy = 0
    for item in vector:
        if q == 0:
            startx = item['x']
            starty = item['y']
        if q == 3: 
            endx = item['x']
            endy = item['y']
        q = q + 1

    # cv2.line(clone, (startx, starty), (endx, endy), (0, 0, 255))

    theta = np.arctan2(starty-endy, startx-endx)
    endpt_ax = int(startx - 1000*np.cos(theta))
    endpt_ay = int(starty - 1000*np.sin(theta))
    endpt_bx = int(endx + 1000*np.cos(theta))
    endpt_by = int(endy + 1000*np.sin(theta))
    gradient.append((starty-endy)/(startx-endx))

    # cv2.line(clone, (startx, starty), (endpt_ax, endpt_ay), (0, 0, 255), 2)
    # cv2.line(clone, (startx, starty), (endpt_bx, endpt_by), (0, 0, 255), 2)

    try:
        angle_tan = (gradient[0]-gradient[2])/(1+gradient[2]*gradient[0])
    except ZeroDivisionError: # vertical
        return 0

    angle = [math.degrees(math.atan(angle_tan)), math.degrees(math.atan(-angle_tan))]
    return angle

    # cv2.imshow(clone)

def from_base64(base64_data):
    nparr = np.fromstring(base64_data.decode('base64'), np.uint8)
    return cv2.imdecode(nparr, cv2.IMREAD_ANYCOLOR)