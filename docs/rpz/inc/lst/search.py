classifier = RandomForestClassifier(n_estimators=300, verbose=2, random_state=0) 
grid_param = { 
     'n_estimators': (100, 300, 500, 800, 1000), 
     'criterion': ['gini', 'entropy'], 
     'bootstrap': [True, False] 
}
gd_sr = GridSearchCV(estimator=classifier,
     param_grid=grid_param, 
     scoring='accuracy', 
     cv=5, 
     n_jobs=-1)
 
clf=gd_sr.fit(feature,labels)
joblib.dump(clf, 'model.joblib')
best_parameters = gd_sr.best_params_ 
print(best_parameters)
best_result = gd_sr.best_score_ 
print(best_result)