import os
from flask import Flask, request, redirect, url_for, flash, send_from_directory
from werkzeug.utils import secure_filename

import numpy as np
import matplotlib.image as mpimg
from tensorflow.keras.models import load_model

UPLOAD_FOLDER = 'E:/Deep/ImageClassification/Static/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
model = load_model("Models/mnist.h5")

app = Flask(__name__, static_folder='C:\\Some\\Directory')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def rgb2gray(rgb):
    return np.dot(rgb[...,:3], [0.2989, 0.5870, 0.1140])


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    path = UPLOAD_FOLDER + filename
    img = mpimg.imread(path)
    gray = rgb2gray(img)
    img = gray.reshape((1, 28, 28, 1))
    pred = np.argmax(model.predict([img]))
    return '<!doctype html><input type="label" value="Result: "><input type="label" value="' + str(pred) + '" disabled>'


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''


if __name__ == '__main__':
    app.run()
