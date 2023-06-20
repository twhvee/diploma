from datetime import timedelta
import numpy as np
import cv2
import sys
import os
import glob
from sklearn import svm
from scipy.stats import mode
import tkinter.filedialog as fd

import shutil


SAVING_FRAMES_PER_SECOND = 10


def format_timedelta(td):
    result = str(td)
    try:
        result, ms = result.split(".")
    except ValueError:
        return "-" + result + ".00".replace(":", "-")
    ms = int(ms)
    ms = round(ms / 1e4)
    return f"-{result}.{ms:02}".replace(":", "-")


def get_saving_frames_durations(cap, saving_fps):
    s = []
    clip_duration = cap.get(cv2.CAP_PROP_FRAME_COUNT) / cap.get(cv2.CAP_PROP_FPS)
    for i in np.arange(0, clip_duration, 1 / saving_fps):
        s.append(i)
    return s


def parserman(tPath):
    hog = cv2.HOGDescriptor()
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

    path2 = tPath + "/man"
    if not os.path.exists(path2):
        os.makedirs(path2)
    count = 0
    imageFrames = getImageList(tPath)
    for imagePath in imageFrames:
        print(imagePath)
        path3 = path2
        path3 += "/" + imagePath[imagePath.find("\\") + 1:] #+ str(count) + ".jpg"
        print(path3)
        image = cv2.imread(imagePath)
        if count == 0:
            imagedraw = cv2.selectROI(image)
        croppedimage = image[int(imagedraw[1]):int(imagedraw[1] + imagedraw[3]),
                       int(imagedraw[0]):int(imagedraw[0] + imagedraw[2])]  # displaying the croppe
        cv2.imwrite(path3, croppedimage)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        count += 1


def getImageList(imageDirectory):
    rImages = glob.glob(imageDirectory + "/*.jpg")
    rImages += glob.glob(imageDirectory + "/*.jpeg")
    rImages += glob.glob(imageDirectory + "/*.png")

    return rImages

def getframe(video_file, dirname):
    filename, _ = os.path.splitext(video_file)
    filename += "-opencv"
    cap = cv2.VideoCapture(video_file)
    fps = cap.get(cv2.CAP_PROP_FPS)
    saving_frames_per_second = min(fps, SAVING_FRAMES_PER_SECOND)
    saving_frames_durations = get_saving_frames_durations(cap, saving_frames_per_second)
    count = 0
    save_count = 0
    while True:
        is_read, frame = cap.read()
        if not is_read:
            break
        frame_duration = count / fps
        try:
            closest_duration = saving_frames_durations[0]
        except IndexError:
            break
        print(closest_duration)
        if frame_duration >= closest_duration:
            frame_duration_formatted = format_timedelta(timedelta(seconds=frame_duration))
            saveframe_name = os.path.join(dirname, f"frame{frame_duration_formatted}.jpg")
            cv2.imwrite(saveframe_name, frame)
            save_count += 1
            try:
                saving_frames_durations.pop(0)
            except IndexError:
                pass
        count += 1

    print(f"Итого сохранено кадров {save_count}")
    return save_count/closest_duration

