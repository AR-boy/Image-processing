import cv2
import os
from cv2 import aruco
import numpy as np

from matplotlib import pyplot as plt
import matplotlib
import shutil

# currently static due to generated board
X_SQUARES = 5
Y_SQUARES = 7
MARKER_LENGTH = 1
SQUARE_LENGTH = 0.8
DICTIONARY = aruco.getPredefinedDictionary(aruco.DICT_6X6_250)

def generateImages(videoCapture) :
    imageDirPath = os.path.join(os.getcwd(), 'calib_images')
    # if os.path.isdir(imageDirPath) :
    #     shutil.rmtree(imageDirPath)
    # os.mkdir(imageDirPath)
    # imageId = 0
    # os.chdir(imageDirPath)

    # while True :
    #     ret, frame = videoCapture.read()
    #     name = str(imageId) + '.jpg'
    #     cv2.imwrite(name, frame)
    #     cv2.imshow("img", frame)
    #     imageId+= 1
    #     if cv2.waitKey(0) & 0xFF == ord('q') :
    #         break

    return np.array([os.path.join(imageDirPath, image) for image in os.listdir(imageDirPath)])

def createCharucoBoard(dictionary) :
    charucoBoardPath = os.path.join(os.getcwd(),'charuco_board.png')
    board = False
    board = aruco.CharucoBoard_create(Y_SQUARES, X_SQUARES, MARKER_LENGTH, SQUARE_LENGTH, dictionary)
    boardImage = board.draw((2000, 2000))
    cv2.imwrite(charucoBoardPath, boardImage)
    # fig = plt.figure()
    # ax = fig.add_subplot(1,1,1)
    # plt.imshow(boardImage, cmap = matplotlib.cm.gray, interpolation = "nearest")
    # ax.axis("off")
    # plt.show()
    print('board: ',board)
    return board

def readImages(calibImages, dictionary, charucoBoard) :
    allIds = []
    allCorners = []
    decimator = 0
    calibCriteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.00001)
    
    for image in calibImages :
        frame = cv2.imread(image)
        grayscaleFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # cv2.imshow('image', frame)
        # cv2.waitKey(1)
        corners, ids, rejectedImgPoints = aruco.detectMarkers(grayscaleFrame, dictionary)
        print('#########')
        print('corners:', corners)
        print('#########')
        if len(corners) > 0 :
            for corner in corners :
                cv2.cornerSubPix(
                    grayscaleFrame,
                    corner,
                    winSize = (3,3),
                    zeroZone = (-1,-1),
                    criteria = calibCriteria
                )
            print('corner: ', corner)
            res2 = cv2.aruco.interpolateCornersCharuco(corners, ids, grayscaleFrame, charucoBoard)
            print('res2: ', res2)
            if res2[1] is not None and res2[2] is not None and len(res2[1])>3 and decimator%1==0:
                allCorners.append(res2[1])
                allIds.append(res2[2])

        decimator+=1

        imSize = grayscaleFrame.shape

        return allCorners, allIds, imSize


def calibrate(videoCapture, dictionary) :

    charucoBoard = createCharucoBoard(dictionary)
    calibImages = generateImages(videoCapture)
    # print('calibImages: ', calibImages)
    allCorners, allIds, imSize = readImages(calibImages, dictionary, charucoBoard)

    cameraMatrixInit = np.array([[ 1000.,    0., imSize[0]/2.],
                                 [    0., 1000., imSize[1]/2.],
                                 [    0.,    0.,           1.]])
    distCoeffsInit = np.zeros((5,1))
    flags = (cv2.CALIB_USE_INTRINSIC_GUESS + cv2.CALIB_RATIONAL_MODEL + cv2.CALIB_FIX_ASPECT_RATIO)
    # print(f'inputs to calibrate camera: allIds: {allIds}, allCorners: {allCorners}, imSize: {imSize}, cameraMatrixInit: {cameraMatrixInit}, distCoeffsInit: {distCoeffsInit} ' )
    (ret, cameraMatrix, distortionCoefficients0,
     rotationVectors, translationVectors,
     stdDeviationsIntrinsics, stdDeviationsExtrinsics,
     perViewErrors) = cv2.aruco.calibrateCameraCharucoExtended(
                      charucoCorners=allCorners,
                      charucoIds=allIds,
                      board=charucoBoard,
                      imageSize=imSize,
                      cameraMatrix=cameraMatrixInit,
                      distCoeffs=distCoeffsInit,
                      flags=flags,
                      criteria=(cv2.TERM_CRITERIA_EPS & cv2.TERM_CRITERIA_COUNT, 10000, 1e-9))

    return ret, cameraMatrix, distortionCoefficients0, rotationVectors, translationVectors


    

# createCharucoBoard(DICTIONARY)
# print('result : ', calibrate(cv2.VideoCapture(0), DICTIONARY))
# while True :
    
#     #  read the screen capture to obtain the frame
#     ret, frame = VideoCapture.read()
#     if cv2.waitKey(1) & 0xFF == ord('q') :
#         break