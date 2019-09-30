# Face_Match_API
A web based service for matching faces using two images, two UUIDs (from redis database), finding top matched images from the database and for finding facial features

## Installation 

1. sudo pip install virtualenv
2. git clone https://github.com/kishansharma3012/Face_Match_API.git
3. cd Face_Match_API
4. virtualenv FaceAPI
Download boost from http://boost.org and proceed to boost root folder
5. ./bootstrap.sh --with-libraries=python
6. ./b2
7. sudo ./b2 install
8. pip install dlib
9. pip install Flask
10. pip install face_recognition
Install Redis server 
11. pip install redis
12. wget http://download.redis.io/redis-stable.tar.gz
13. tar xvzf redis-stable.tar.gz
14. cd redis-stable
15. make





