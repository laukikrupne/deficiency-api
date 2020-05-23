import os
from flask import Flask, flash, request, redirect, url_for, jsonify, render_template
from werkzeug.utils import secure_filename
import cv2
import numpy as np
import keras
from keras.models import load_model
from keras import backend as K

UPLOAD_FOLDER = './uploads/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



dict =               {"[0]": "Apple___Apple_scab", 
                      "[1]": "Apple___Black_rot",
                      "[2]": "Apple___Cedar_apple_rust",
                      "[3]": "Apple___healthy",
                      "[4]": "Blueberry___healthy",
                      "[5]": "Cherry_(including_sour)___Powdery_mildew",
                      "[6]": "Cherry_(including_sour)___healthy",
                      "[7]": "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot",
                      "[8]": "Corn_(maize)___Common_rust_",
                      "[9]": "Corn_(maize)___Northern_Leaf_Blight",
                      "[10]": "Corn_(maize)___healthy",
                      "[11]": "Grape___Black_rot",
                      "[12]": "Grape___Esca_(Black_Measles)",
                      "[13]": "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)",
                      "[14]": "Grape___healthy",
                      "[15]": "Orange___Haunglongbing_(Citrus_greening)",
                      "[16]": "Peach___Bacterial_spot",
                      "[17]": "Peach___healthy",
                      "[18]": "Pepper,_bell___Bacterial_spot",
                      "[19]": "Pepper,_bell___healthy",
                      "[20]": "Potato___Early_blight",
                      "[21]": "Potato___Late_blight",
                      "[22]": "Potato___healthy",
                      "[23]": "Raspberry___healthy",
                      "[24]": "Soybean___healthy",
                      "[25]": "Squash___Powdery_mildew",
                      "[26]": "Strawberry___Leaf_scorch",
                      "[27]": "Strawberry___healthy",
                      "[28]": "Tomato___Bacterial_spot",
                      "[29]": "Tomato___Early_blight",
                      "[30]": "Tomato___Late_blight",
                      "[31]": "Tomato___Leaf_Mold",
                      "[32]": "Tomato___Septoria_leaf_spot",
                      "[33]": "Tomato___Spider_mites Two-spotted_spider_mite",
                      "[34]": "Tomato___Target_Spot",
                      "[35]": "Tomato___Tomato_Yellow_Leaf_Curl_Virus",
                      "[36]": "Tomato___Tomato_mosaic_virus",
                      "[37]": "Tomato___healthy"}

def allowed_file(filename):
	return '.' in filename and \
		   filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
	if request.method == 'POST':
		# check if the post request has the file part
		if 'file' not in request.files:
			flash('No file part')
			return redirect(request.url)
		file = request.files['file'].read()
		# if user does not select file, browser also
		# submit an empty part without filename
		if file.filename == '':
			flash('No selected file')
			return redirect(request.url)
		if file and allowed_file(file.filename):
			nparr = np.fromstring(file, np.uint8)
			img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
			classifier = load_model('./models/128_vgg_16.h5')
			image = cv2.resize(img, (128, 128), interpolation = cv2. INTER_LINEAR)
			image = image / 255.
			image = image.reshape(1,128,128,3)
			res = str(np.argmax(classifier.predict(image, 1, verbose = 0), axis=1))
			K.clear_session()
			result = dict[res]
			return jsonify({"Deficiency": result} )
	return '''
	<!doctype html>
	<title>OK</title>
	<h1>OK!!!</h1>'''

if __name__ == "__main__":
	app.run()