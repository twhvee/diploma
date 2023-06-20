def parserman(tPath):
    hog = cv2.HOGDescriptor()
    hog.setSVMDetector(
	cv2.HOGDescriptor_getDefaultPeopleDetector())
    path2 = tPath + "/man"
    if not os.path.exists(path2):
        os.makedirs(path2)
    count = 0
    imageFrames = getImageList(tPath)
    for imagePath in imageFrames:
        path3 = path2 + "/" + str(count) + ".jpg"
        image = cv2.imread(imagePath)
        if count == 0:
            imagedraw = cv2.selectROI(image)
        croppedimage = image[int(imagedraw[1]):int(imagedraw[1]+imagedraw[3]), int(imagedraw[0]):int(imagedraw[0]+imagedraw[2])] 
        cv2.imwrite(path3, croppedimage)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        count += 1