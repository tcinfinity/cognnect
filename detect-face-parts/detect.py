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
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

def faceangle(image):
  image = cv2.imread(image)
  image = imutils.resize(image, width=500)
  gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

  rects = detector(gray, 1)

  vector = []

  for (i, rect) in enumerate(rects):
    shape = predictor(gray, rect)
    shape = face_utils.shape_to_np(shape)

    for (name, (i, j)) in FACIAL_LANDMARKS_IDXS.items():
      clone = image.copy()
#       cv2.putText(clone, name, (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
#       0.7, (0, 0, 255), 2)

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

  theta = np.arctan2(starty-endy, startx-endx)
  endpt_ax = int(startx - 1000*np.cos(theta))
  endpt_ay = int(starty - 1000*np.sin(theta))
  endpt_bx = int(endx + 1000*np.cos(theta))
  endpt_by = int(endy + 1000*np.sin(theta))
  
  try:
    gradient = (starty-endy)/(startx-endx)
    angle = math.degrees(math.atan(gradient))
    if angle > 0:
      return 90-angle
    else:
      return 90+angle
  except ZeroDivisionError:
    return 0
  

print(faceangle('images/example_01.jpg'))
print(faceangle('images/example_02.jpg'))
print(faceangle('images/example_03.jpg'))