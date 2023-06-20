
import os
import urllib.request
from typing import List

from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from makeframes import getframe, parserman
import shutil
from hogimg import make_hog_video
from hogdescriptor import  featureExtraction, getSportsActionName
from scipy.stats import mode
import joblib

UPLOAD_FOLDER = 'static/uploads/'
HOG_FOLDER = 'static/hogHist/'

app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['HOG_FOLDER'] = HOG_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

clf = joblib.load('modelgood.joblib')
@app.route('/')
def upload_form():
	return render_template('index.html')

@app.route('/', methods=['POST'])
def upload_video():
	mas: List[str] = []
	if 'file' not in request.files:
		flash('No file part')
		return redirect(request.url)
	file = request.files['file']
	if file.filename == '':
		flash('No image selected for uploading')
		return redirect(request.url)
	else:
		filename = secure_filename(file.filename)
		filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
		file.save(filepath)
		path = os.path.join(app.config['HOG_FOLDER'], filename[:-3])
		if not os.path.exists(path):
			os.mkdir(path)
			fps = getframe(filepath, path)
			make_hog_video(path, fps)
			parserman(path)
		vFeatures = featureExtraction(path, '','Test')
		predictedLabels = clf.predict(vFeatures)
		predictedLabelMode = (mode(predictedLabels))[0]
		nameact = getSportsActionName(predictedLabelMode)

		mas.append(filename)
		mas.append('mygeneratedvideo.mp4')

		return render_template('index.html', filename=mas, nameact=nameact)

@app.route('/info_page', methods=['GET'])
def info_page():
    return render_template('info.html')


@app.route('/display/<filename>')
def display_video(filename):
	print(filename)
	return redirect(url_for('static', filename='uploads/' + filename), code=301)

@app.route('/display2/<filename>')
def display_video2(filename):
	print(filename)
	return redirect(url_for('static', filename='uploads/' + filename), code=301)

@app.route('/playex/<filename>')
def play_ex(filename):
	print(filename)
	return redirect(url_for('static', filename='examples/' + filename), code=301)


@app.route('/play/<filename>')
def video_play(filename):
	print(filename)
	return redirect(url_for('static', filename='uploads/' + filename), code=301)

if __name__ == "__main__":
    app.run(debug=True)





# See PyCharm help at https://www.jetbrains.com/help/pycharm/
