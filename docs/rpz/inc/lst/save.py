def get_file_features(sportsActionName):
    sportsActionFeatures = []
    firstActionFlag = 0
    sportsActionDir = sportsActionPath + "/" + sportsActionName
    sportsActionFeatures = []
    videoList = getListOfDir(sportsActionDir)
    videoCount = 1
    videoFeatures = []
      
    for video  in videoList:
        videoPath = sportsActionDir + "/" + video 
        videoFeatures = featureExtraction(videoPath , sportsActionName, 'Trng')        
        if firstActionFlag == 0:
            sportsActionFeatures = videoFeatures
            firstActionFlag = 1
        else:
            sportsActionFeatures = np.concatenate( (sportsActionFeatures, videoFeatures), axis=0)
        videoCount += 1
    with open(f'{sportsActionName}.npy', 'wb') as f:
        np.save(f, sportsActionFeatures)