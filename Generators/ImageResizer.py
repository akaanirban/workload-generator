import cv2
import sys
import os
import subprocess


SOURCEIMAGEDIRNAME = "/home/anirban/Pictures/First200"
DESTIMAGEDIRNAME = "/home/anirban/Pictures/First200_resized"
CAMERA_RESOLUTION = (640, 480)


if __name__ == "__main__":

    response = subprocess.run(['mkdir', DESTIMAGEDIRNAME], 
	                          shell = False, stderr=subprocess.PIPE)

    for imagefile in os.listdir(SOURCEIMAGEDIRNAME):
        image = cv2.imread(os.path.join(SOURCEIMAGEDIRNAME, imagefile))
        resized_image = cv2.resize(image, CAMERA_RESOLUTION)
        cv2.imwrite(DESTIMAGEDIRNAME + os.sep + imagefile, resized_image)


        