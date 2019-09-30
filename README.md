# Face_Match_API
A web based service for matching faces using two images, two UUIDs (from redis database), finding top matched images from the database and for finding facial features. This API uses face recognition library (https://pypi.org/project/face_recognition/)
for matching the faces and for finding the facial features. It uses dlib's state-of-the-art face recognition built with deep learning. The model has an accuracy of 99.38% on the Labeled Faces in the Wild benchmark.


## Installation 

1. sudo pip install virtualenv
2. git clone https://github.com/kishansharma3012/Face_Match_API.git
3. cd Face_Match_API
4. virtualenv FaceAPI
5. ./bootstrap.sh --with-libraries=python // Install Boost library from http://boost.org and then proceed to the boost folder
6. ./b2
7. sudo ./b2 install
8. pip install dlib
9. pip install Flask
10. pip install face_recognition
11. pip install redis // Install Redis server 

## Database
Both Redis and Sqlite3 database can be used. 

# Features

## Upload 
User can upload the image in the database by simply browsing the image, providing the user name and clicking the button Upload. The API only allows images with only one face, and it discards the upload if images with no face or more than 1 faces are uploaded. 

<img src="https://github.com/kishansharma3012/Face_Match_API/blob/master/etc/images_readme/upload1.png" width="500">
<img src="https://github.com/kishansharma3012/Face_Match_API/blob/master/etc/images_readme/upload2.png" width="500">

## Face match images
User can upload two photos, and match the face in the photos by simply clicking Match them button. It will show the probability of the face match. 

<img src="https://github.com/kishansharma3012/Face_Match_API/blob/master/etc/images_readme/facematch_Img.png" width="500">

## Face match ID
User can match two already uploaded image in the database by simply providing their UUID's.

<img src="https://github.com/kishansharma3012/Face_Match_API/blob/master/etc/images_readme/facematch_ID.png" width="500">

## Face match Database
User can check the images which are the nearest neighbour to the uploaded image.

<img src="https://github.com/kishansharma3012/Face_Match_API/blob/master/etc/images_readme/facematch_DB.png" width="500">


## Facial features
User can check the facial features/ landmarks (such as Chin, Jawline, eyes, eyebrows, upper lip and lower lip) of the uploaded image

<img src="https://github.com/kishansharma3012/Face_Match_API/blob/master/etc/images_readme/facial_features.png" width="500">

