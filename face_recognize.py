# Face Recognizing Main Function should be run after create_dataset.py

import cv2, sys, numpy, os
size = 4

datasets = 'datasets'

# Model Loading...
print('Recognizing Face Please Be in sufficient Lights...')

# Create a list of images and a list of corresponding names
(images, labels, names, id) = ([], [], {}, 0)
for (subdirs, dirs, files) in os.walk(datasets):
    for subdir in dirs:
        names[id] = subdir
        subjectpath = os.path.join(datasets, subdir)
        for filename in os.listdir(subjectpath):
            path = subjectpath + '/' + filename
            label = id
            images.append(cv2.imread(path, 0))
            labels.append(int(label))
        id += 1
(width, height) = (130, 100)

# Create a Numpy array from the two lists above
(images, labels) = [numpy.array(lis) for lis in [images, labels]]

# OpenCV trains a model from the images
# "pip install opencv-contrib-python" run this command for cv2.face
# LBPH ALgorithm used
model = cv2.face.LBPHFaceRecognizer_create()
model.train(images, labels)

# Webcam Stream
face_cascade = cv2.CascadeClassifier(os.path.join(cv2.data.haarcascades, 'haarcascade_frontalface_default.xml'))
webcam = cv2.VideoCapture(0)
while True:
    (_, im) = webcam.read()
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        cv2.rectangle(im, (x, y), (x + w, y + h), (255, 0, 0), 2)
        face = gray[y:y + h, x:x + w]
        face_resize = cv2.resize(face, (width, height))
        # Try to recognize the face
        prediction = model.predict(face_resize)
        cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0), 3)

        if prediction[1]<500:
            cv2.putText(im, '% s - %.0f' %(names[prediction[0]], prediction[1]), (x-10, y-10),cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0))
        else:
            cv2.putText(im, 'not recognized',(x-10, y-10), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0))
 
    cv2.imshow('OpenCV', im)
    
    key = cv2.waitKey(10)
    if key == 27:
        break
