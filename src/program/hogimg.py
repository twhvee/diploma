import skimage
from skimage import feature
import cv2
import sys
import os
import glob
import matplotlib.pyplot as plt
from datetime import timedelta
import numpy as np
import joblib
from sklearn import svm
from scipy.stats import mode
import sys

def getImageList(imageDirectory):
    # Find different type of images
    rImages = glob.glob(imageDirectory + "/*.jpg")
    rImages += glob.glob(imageDirectory + "/*.jpeg")
    rImages += glob.glob(imageDirectory + "/*.png")

    return rImages

def make_contrast(path):
    count = 0
    imageFrames = getImageList(path)
    for iFrame in imageFrames:
        saveframe_name = path + "/" + iFrame[iFrame.find("\\") + 1:]
        print(iFrame)
        hog_image = cv2.imread(iFrame)
        lab = cv2.cvtColor(hog_image, cv2.COLOR_BGR2LAB)
        l_channel, a, b = cv2.split(lab)

        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        cl = clahe.apply(l_channel)

        limg = cv2.merge((cl, a, b))

        enhanced_img = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
        cv2.imwrite(saveframe_name, enhanced_img)
        count += 1


def generate_video(path, fps):
    video_name = "static/uploads" + '/mygeneratedvideo.mp4'

    make_contrast(path)
    imageFrames = getImageList(path)
    frame = cv2.imread(imageFrames[0])
    height, width, layers = frame.shape
    print(fps)
    video = cv2.VideoWriter(video_name, 0, fps , (width, height))
    for iFrame in imageFrames:
        video.write(cv2.imread(iFrame))

    cv2.destroyAllWindows()
    video.release()

def make_hog_video(path, fps):
    path2 = path + "/hog"

    if not os.path.exists(path2):
        os.makedirs(path2)
    count = 0
    imageFrames = getImageList(path)
    for iFrame in imageFrames:
        saveframe_name = path2 + "/" + iFrame[iFrame.find("\\") + 1:]  #"/" + str(count) + ".jpg"
        image = cv2.imread(iFrame)

        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        img_gray = skimage.color.rgb2gray(image)

        (hog, hog_image) = feature.hog(img_gray, orientations=9,
                                       pixels_per_cell=(8, 8), cells_per_block=(2, 2),
                                       block_norm='L2-Hys', visualize=True, transform_sqrt=True)

        cv2.imwrite(saveframe_name, hog_image * 255.)
        count += 1
    cv2.waitKey(0)

    generate_video(path2, fps)