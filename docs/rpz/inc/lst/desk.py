def featureExtraction(videoPath, actionName, type):
    framePath = videoPath
    if os.path.exists( framePath + "/man") :
        framePath += "/man/"
    imageFrames = getImageList(framePath)
    frameCount = 0
    videoFeatures  = []
    for iFrame in imageFrames:
        frame = cv2.imread(iFrame)
        gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        height, width = 256, 256
        hogDescriptor = cv2.HOGDescriptor((width, height), (16, 16), (8,8), (8,8), 9)

        if gray.shape != (height, width):
            gray = cv2.resize(gray, (width, height))    

        hist = hogDescriptor.compute(gray,(8,8))     
        sortedHogHist = np.sort(hist, axis=None)
        keyFeatures = sortedHogHist[- featuresLimit : ]

        if type == "Trng":
            print(sportsActionTag[actionName])
            keyFeatures = np.insert(keyFeatures, 0, sportsActionTag[actionName])
        
        videoFeatures.append(keyFeatures)
        if frameCount >= 25:
            break
        frameCount += 1
    
    return videoFeatures