"""
Original Author: Life2coding / https://www.life2coding.com/crop-image-using-mouse-click-movement-python/
Modified By: Marco Knabe
Modifications:  put into class structure
                added 3 additional 3 draw directions
                outputs cropped image as file 
                checks is output file already exists
                scals shown cropped image
"""

import cv2
import numpy as np
from pathlib import Path

class CropImage:
    cropping = False
    x_start, y_start, x_end, y_end = 0, 0, 0, 0
    image = None
    oriImage = None
    outputFileName = 'crop'
    outputFileExtension = '.png'
    scaleValue = 8

    def __init__(self, imageName):
        self.image = cv2.imread(imageName)
        self.oriImage = self.image.copy()
        cv2.namedWindow("image")
        cv2.setMouseCallback("image", self.mouse_crop)
        scaleFactor = 1
        while True:
            i = self.image.copy()
            if scaleFactor < 0.1:
                scaleFactor = 0.1
            if cv2.getWindowProperty("image", cv2.WND_PROP_VISIBLE) <1:
                break
            if cv2.waitKey(33) == 27:
                break
            if not self.cropping:
                cv2.imshow("image", self.image)
            elif self.cropping:
                cv2.rectangle(i, (self.x_start, self.y_start), (self.x_end, self.y_end), (255, 0, 0), 2)
                cv2.imshow("image", i)
            cv2.waitKey(1)
        cv2.destroyAllWindows()

    def mouse_crop(self, event, x, y, flags, param):
        # grab references to the global variables
        global x_start, y_start, x_end, y_end, cropping
        # if the left mouse button was DOWN, start RECORDING
        # (x, y) coordinates and indicate that cropping is being
        if event == cv2.EVENT_LBUTTONDOWN:
            self.x_start, self.y_start, self.x_end, self.y_end = x, y, x, y
            self.cropping = True
        # Mouse is Moving
        elif event == cv2.EVENT_MOUSEMOVE:
            if self.cropping == True:
                self.x_end, self.y_end = x, y
        # if the left mouse button was released
        elif event == cv2.EVENT_LBUTTONUP:
            # record the ending (x, y) coordinates
            self.x_end, self.y_end = x, y
            self.cropping = False # cropping is finished
            refPoint = [(self.x_start, self.y_start), (self.x_end, self.y_end)]
            if len(refPoint) == 2: #when two points were found
                roi = None
                if(refPoint[0][0] > refPoint[1][0]):
                    if(refPoint[0][1] < refPoint[1][1]):
                        roi = self.oriImage[refPoint[0][1]:refPoint[1][1], refPoint[1][0]:refPoint[0][0]]
                    if(refPoint[0][1] > refPoint[1][1]):
                        roi = self.oriImage[refPoint[1][1]:refPoint[0][1], refPoint[1][0]:refPoint[0][0]]
                if(refPoint[0][0] < refPoint[1][0]):
                    if(refPoint[0][1] < refPoint[1][1]):
                        roi = self.oriImage[refPoint[0][1]:refPoint[1][1], refPoint[0][0]:refPoint[1][0]]
                    if(refPoint[0][1] > refPoint[1][1]):
                        roi = self.oriImage[refPoint[1][1]:refPoint[0][1], refPoint[0][0]:refPoint[1][0]]

                outputFile = Path(self.outputFileName + self.outputFileExtension)
                fileNameCounter = 0
                while outputFile.is_file():
                    fileNameCounter+=1
                    outputFile = Path(self.outputFileName + str(fileNameCounter) + self.outputFileExtension)    

                if(fileNameCounter > 0):
                    print('Output File Name: ' + self.outputFileName + str(fileNameCounter) + self.outputFileExtension)
                    cv2.imwrite(self.outputFileName + str(fileNameCounter) + self.outputFileExtension, roi)
                else:
                    print('Output File Name: ' + self.outputFileName + self.outputFileExtension)
                    cv2.imwrite(self.outputFileName + self.outputFileExtension, roi)

                scaleX = self.scaleValue
                scaleY = self.scaleValue
                scaleUp = cv2.resize(roi, None, fx= scaleX, fy= scaleY)
                cv2.imshow("Cropped", scaleUp)