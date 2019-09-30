# Face Match API By @Kishan
# app.py -->  Flask application for Face Match API 
# Run file --> python app.py

# Importing libraries and classes
from flask import Flask, json, Response, request, render_template
from os import path, getcwd
from db import Database_Sqlite, Database_Redis
from face import Face
import uuid 
import sqlite3

# Initializing Flask application
app = Flask(__name__)
app.config['file_allowed'] = ['image/png', 'image/jpeg']

# Initializing database
app.db =  Database_Redis()

# Initialzing facial recognition class
app.face = Face()

def success_handle(output, status=200, mimetype='application/json'):
    """
        Function : for handling Success message
        Input    : output -> output message
                   status -> status code
                   mimetype -> 'application/json'
        Output   : Response -> success message (JSON)
    """
    return Response(output, status=status, mimetype=mimetype)

def error_handle(error_message, status=500, mimetype='application/json'):
    """
        Function : for handling error message
        Input    : output -> output message
                   status -> status code
                   mimetype -> 'application/json'
        Output   : Response -> Error message (JSON)
    """
    return Response(json.dumps({"error": {"message": error_message}}), status=status, mimetype=mimetype)

@app.route('/', methods=['GET'])
def homepage_UI():
    """
        Function : Router for Homepage with User interface
    """
    return render_template('index.html')

@app.route('/api', methods=['GET'])
def homepage():
    """
        Function : Homepage Without User interface (use API via POSTMAN)
    """
    output = json.dumps({"api": '1.0'})
    return success_handle(output)

@app.route('/api/upload', methods=['POST'])
def upload():
    """
        Function : Router for uploading image (only one face per image) with user name into the database
        Input    : Request (Imagefile and name)
        Output   : Success (Image Uploaded) or Error Message
    """
    # Checking if the image file is provided 
    if 'imagefile' not in request.files:
        print ("Please upload Image file")
        return error_handle("Please upload Image file")
    else:
        print("File request", request.files)
        file = request.files['imagefile']

        # Checking if the uploaded image file extension is allowed
        if file.mimetype not in app.config['file_allowed']:
            print("File extension is not allowed")
            return error_handle("Please upload file with *.png , *.jpg")
        else:
            img_file = file.read()
            # Checking num of faces in the image
            num_faces = app.face.num_faces(img_file)
            if num_faces == 0:
                print("Error : Uploaded image has no face!!")
                return error_handle("Error : Uploaded image has no face. Upload again")
            elif num_faces > 1:
                print("Error : Uploaded image has more than 1 face. Upload again.")
                return error_handle("Error : Uploaded image has more than 1 face. Upload again")
                
            # Creating unique UUID 
            id_ = uuid.uuid1()
            name = request.form['name']

            # Inserting image in the database
            image_id = app.db.insert(id_, img_file, name)
            if image_id:
                return_output = json.dumps({"image_id": id_, "name": name})
                return success_handle(return_output)
            else:
                print("Error inserting image in the database!!")
                return error_handle("Error inserting image in the database!!")

        print("Image uploaded to database!!")

@app.route('/api/FaceMatch_ID', methods=['POST'])
def FaceMatch_ID():
    """
        Function : Router for matching 2 images using UUID from the database
        Input    : Request (Json file with list of 2 UUIDs from database)
        Output   : Success (Face match Probability and 2 Images as Base64 encoded string) or Error message
    """

    if len(request.get_json()['images']) != 2:
        return error_handle("Error: Enter two uuids")        
    # Extracting UUID from the request
    uuid_1 = request.get_json()['images'][0]
    uuid_2 = request.get_json()['images'][1]

    # Checking for 2 UUIDs 
    if not uuid_1 or not uuid_2 :
        return error_handle("Error: Enter two uuids")
    else:
        # Finding Images and user name from database corresponding to UUIDs
        result_1, user_name1 = app.db.select(uuid_1)
        result_2, user_name2 = app.db.select(uuid_2)

        # Checking if the UUIDs are in the database
        if not result_1:
            return error_handle("Uuid 1 not found in Database")
        if not result_2:
            return error_handle("Uuid 2 not found in Database")

        # Comparing face in both images
        probability, img_string1, img_string2, _  = app.face.compare(result_1, [result_2])

        if probability is not None:
            Prob_msg = str(user_name1) + "\t" + str(user_name2) + "with probability: \t" + str(round(probability[0],2))
            message = {"FaceMatch_ID":{"image1":img_string1, "image2": img_string2, "probability": Prob_msg}}
            return success_handle(json.dumps(message))
        else:
            return error_handle("Error in comparing images !!")

@app.route('/api/FaceMatch_Image', methods=['POST'])
def FaceMatch_Image():
    """
        Function : Router for matching 2 images (direct input)
        Input    : Request (2 imagefiles [imagefile1, imagefile2])
        Output   : Success (Face match Probability ) or Error message
    """

    # Checking imagefile in the requested files
    if 'imagefile1' not in request.files:
        print ("Please upload Image file 1")
        return error_handle("Please upload Image file 1")
    elif 'imagefile2' not in request.files:
        print ("Please upload Image file 2")
        return error_handle("Please upload Image file 2")
    else:
        file1 = request.files['imagefile1']
        file2 = request.files['imagefile2']

        # Checking if the uploaded files are allowed
        if file1.mimetype not in app.config['file_allowed'] and file2.mimetype not in app.config['file_allowed']:
            print("File extension is not allowed")
            return error_handle("Please upload file with *.png , *.jpg")    

        # Comparing two images
        probability, _, _ , _  = app.face.compare(file1.read(), [file2.read()])

        if probability is not None:
            message = {"FaceMatch_Image":{"probability": float("{0:.2f}".format(probability[0]))}}
            return success_handle(json.dumps(message))
        else:
            return error_handle("Error in comparing images !!")

@app.route('/api/FaceMatch_DB', methods=['POST'])
def FaceMatch_DB():
    """
        Function : Router for matching uploaded image with images from the database
        Input    : Request (imagefile)
        Output   : Success (Face match Probabilities (top3) and 3 matched mages as Base64 encoded string) or Error message
    """

    # Checking imagefile in the requested files
    if 'imagefile' not in request.files:
        print ("Please upload Image file ")
        return error_handle("Please upload Image file ")
    
    else:
        print("File request", request.files)
        file = request.files['imagefile']
        
        # Checking if the uploaded files are allowed
        if file.mimetype not in app.config['file_allowed'] :
            print("File extension is not allowed")
            return error_handle("Please upload file with *.png , *.jpg")

        # Selecting all the images and user names from the database for face comparison
        img_bytes = []
        user_names = []
        for uuid in app.db.connection.keys():
            img_ , user = app.db.select(uuid)
            img_bytes.append(img_)
            user_names.append(user)
        
        # Comparing face in the uploaded image with all the images in the database
        probability, _, img_strings, indices  = app.face.compare(file.read(), img_bytes)

        if probability is not None:
            prob_message = "Top matced Faces : \t " + str(user_names[indices[-1]]) + ":" + str(round(probability[0],2)) + "\t8" + \
                            str(user_names[indices[-2]]) + ":" + str(round(probability[1],2)) + "\t8" + \
                            str(user_names[indices[-3]]) + ":" + str(round(probability[2],2))
              
            message = {"FaceMatch_DB":{"images":img_strings, "probability": prob_message}}
            return success_handle(json.dumps(message))
        else:
            return error_handle("Error in comparing images !!")

@app.route('/api/FaceFeature', methods=['POST'])
def FaceFeature():
    """
        Function : Router for finding face feature in the image (direct input)
        Input    : Request (1 imagefile)
        Output   : Success (img_feat: Image with facial features encoded as Base64  string) or Error message
    """
    # Checking imagefile in the requested files
    if 'imagefile' not in request.files:
        print ("Please upload Image file")
        return error_handle("Please upload Image file ")
    else:
        print("File request", request.files)
        file = request.files['imagefile']
        # Checking if the uploaded file is allowed
        if file.mimetype not in app.config['file_allowed'] :
            print("File extension is not allowed")
            return error_handle("Please upload file with *.png , *.jpg")    
        
        # Computing facial features
        img_feat = app.face.facial_landmarks(file.read())
        
        if img_feat is not None:
            message = {"FaceFeature":{"img_feat": img_feat}}
            return success_handle(json.dumps(message))
        else:
            return error_handle("Error in finding feature from the image")


# Run the app
app.run(debug=True)
