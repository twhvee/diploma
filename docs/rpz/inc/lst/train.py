def main():
	flag = 0
	sportsActionFeatures = []
	
	for actName in ('bending_back', 'BodyWeightSquats', 'front_raises', 'JumpingJack', 'lunge', 'pull_ups', 'push_up', 'situp', 'stretching_leg', 'swinging_legs'):
		desc_arr = np.load(f'{actName}.npy')
		if flag == 0:
			sportsActionFeatures = desc_arr
			flag = 1
		else:
			print(desc_arr)
			sportsActionFeatures  = np.concatenate((sportsActionFeatures, desc_arr), axis=0)
	np.random.shuffle(sportsActionFeatures)
	labels = []
	feature = []
	for featureAndLabel in sportsActionFeatures:
		labels.append(int(featureAndLabel[0]))
		feature.append((np.delete(featureAndLabel, 0)).tolist())
		
	clf=RandomForestClassifier(n_estimators=1000, verbose=2,n_jobs=10, bootstrap=False, criterion='entropy')
	clf.fit(feature,labels)
	joblib.dump(clf, 'model.joblib')