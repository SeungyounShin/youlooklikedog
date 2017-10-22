
# A very simple Flask Hello World app for you to get started with...

import os,time
from flask import Flask, render_template
from werkzeug import secure_filename
from flask import send_from_directory,request,redirect, url_for

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '/home/dogbreadidentification/mysite/images'
path = '/home/dogbreadidentification/mysite/images'

@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)

@app.route('/result/<filename>')
def result(filename):
    path = '/home/dogbreadidentification/mysite/images/'+filename
    from predict_resnet50 import predict
    print("import predict.py from local server")
    start = time.time()
    try:
        breed = predict(path)
    except:
        breed = "error occured while predicting..."
    print("result : ",breed, "\nit tooks :",time.time()-start,"sec")
    return render_template('result.html',breed=breed)

@app.route('/')
def upload():
   print("trying to upload file...")
   return render_template('upload.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],filename)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for("result", filename=filename),)
    return redirect(url_for('upload'))


if __name__ == '__main__':
   app.run(debug = True)