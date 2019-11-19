import cv2
from cv2 import aruco
import numpy as np
from matplotlib import pyplot as plt

from calibration import calibrate
#  define video capture output
cap = cv2.VideoCapture(0)
# define the dictionary to use
dictionary = aruco.getPredefinedDictionary(aruco.DICT_6X6_250)

# calibrate camera
retro, cameraMatrix, distortionCoefficients0, rotationVectors, translationVectors = calibrate(cap, dictionary)
# frame loop
while(True) :

    #  read the screen capture to obtain the frame
    ret, frame = cap.read()

    # given the frame and dictionairy, detect markers 
    # corners, ids, rejectedImgPoints = aruco.detectMarkers(frame, dictionary)
    
    # draw detected markers on the frame
    

    # rvecs, tvecs, bullshit = aruco.estimatePoseSingleMarkers(corners, 0.0285 , cameraMatrix, distortionCoefficients0)

    # processesedFrame = aruco.drawDetectedMarkers(frame.copy(), corners, ids)
    # # print('aca:', frame, cameraMatrix, distortionCoefficients0, rotationVectors, translationVectors, 0.1)

    # for i in range(len(tvecs)) :
    #     print('fuck you asshole', len(translationVectors))
    #     processesedFrame = cv2.aruco.drawAxis(processesedFrame, cameraMatrix, distortionCoefficients0, rvecs[i], tvecs[i], 0.1)

    # show the frame via screen 
    # cv2.imshow('image frame', processesedFrame)
    # plt.figure()
    # plt.imshow(imaxis)
    # plt.grid()
    # plt.show()
    # cv2.undistort('./calib_images/', cameraMatrix,distortionCoefficients0 )

    undistortedFrame = cv2.undistort(cv2.imread('./calib_images/17.jpg'), cameraMatrix, distortionCoefficients0)
    # wait till the frame is displayed and if q key is pressed stop the loop
    while True :
        cv2.imshow('image undistorted', undistortedFrame)
        cv2.imshow('image distorted', cv2.imread('./calib_images/17.jpg'))
        if cv2.waitKey(1) and 0xFF == ord('q') :
            break
    