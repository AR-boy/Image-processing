import cv2
from cv2 import aruco
import numpy as np
from matplotlib import pyplot as plt

cap = cv2.VideoCapture(0)

while(True) :

    #  read the screen capture to obtain the frame
    ret, frame = cap.read()
    
    # define the dictionary to use
    dictionary = aruco.getPredefinedDictionary(aruco.DICT_6X6_250)
    
    # given the frame and dictionatr, detect markers 
    corners, ids, rejectedImgPoints = aruco.detectMarkers(frame, dictionary)
    
    # draw detect markers on the frame
    frame_markers = aruco.drawDetectedMarkers(frame.copy(), corners, ids)

    # show the frame via screen 
    cv2.imshow('image frame', frame_markers)

    # wait till the frame is displayed and if q key is pressed stop the loop
    if cv2.waitKey(1) & 0xFF == ord('q') :
        break
    