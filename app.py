import cv2
from deepface import DeepFace

from flask import Flask, session
from flask import Flask, flash, request, redirect, url_for

import os
from os.path import join, dirname, realpath

from werkzeug.utils import secure_filename


UPLOAD_FOLDER = join(dirname(realpath(__file__)), 'static/temp/')
PARENT_DIR = join(dirname(realpath(__file__)), 'static/users/')

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def face_recognition():
   return 'Welcome to Face Recognition Module'

@app.route('/createUser', methods= ['POST'])
def createUser():
   directory = request.form['id']
   
   if(directory in (os.listdir(PARENT_DIR))):
      return 'User Already Exists'

   path = os.path.join(PARENT_DIR, directory)  
   os.mkdir(path)  

   return 'User Directory Created Successfully'

@app.route('/testImage', methods = ['POST'])
def test_image():
      if 'file' not in request.files:
         flash('No file part')
         return redirect(request.url)
        
      file = request.files['file']
      directory=request.form['id']

      if file.filename == '':
         flash('No selected file')
         return redirect(request.url)
      
      if file and allowed_file(file.filename):
         filename = secure_filename(file.filename)
         print(filename)
         file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
         
         img = join(app.config['UPLOAD_FOLDER'], filename)
         db = join(PARENT_DIR, directory)
         entries = os.listdir(db)

         if(len(entries)==0):
            return 'No Label Found'


         df=DeepFace.find(img_path=img,db_path=db)

         if(df.size==0):
            return 'No Label Found'
         
         print(df)
         return 'Label Found: '+os.path.splitext(os.path.basename(df['identity'][0]))[0]
              


@app.route('/addImage', methods = ['POST'])
def add_image():
   if 'file' not in request.files:
      flash('No file part')
      return redirect(request.url)
      
   file = request.files['file']
   directory=request.form['id']
   name=request.form['name']+'.jpg'

   if file.filename == '':
      flash('No selected file')
      return redirect(request.url)
   
   if file and allowed_file(file.filename):
      filename = secure_filename(file.filename)
      print(filename)

      db = join(PARENT_DIR, directory)
      file.save(os.path.join(db, name))
      
      # img = join(app.config['UPLOAD_FOLDER'], filename)

      # detected_face = DeepFace.detectFace(img, detector_backend = 'mtcnn')
      
      # if(detected_face is not None):

      #    db = join(PARENT_DIR, directory)
      #    file.save(os.path.join(db, filename))

      return "Face Uploaded Successfully to User's Known Person List"
      
      # return  "No Face Found"


if __name__ == '__main__':
   app.secret_key = 'dhruv123'
   app.run()

