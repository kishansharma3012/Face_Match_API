# Face Match API By @Kishan
# face.py -->  Machine learning/ Computer Vision based function for Face recognition
 
# Importing Libraries
import face_recognition
from os import path
import io
from PIL import Image, ImageDraw
import numpy as np
import base64


# Class Face : For face comparison and feature extraction methods
class Face:
    def compare(self,image, images):
        """
        Function : for comparing face in image with the faces in images
        Input    : image  -> image
                   images -> list of images (for search in database) 
        Output   : probability -> list of top matched probablitiy (upto 3)
                   img_str     -> Base64 encoded string of the image file
                   img_strs    -> list of top matched Base64 encoded string of the image file
                   indices     -> sorted indices of top matched face in the images list
        """
        # Image in bytes format
        image = io.BytesIO(image)
        images = [io.BytesIO(image_) for image_ in images]

        # Bytes to PIL Image
        img_pil = Image.open(image)
        img_pils = [Image.open(image_) for image_ in images]

        # PIL image to numpy array
        img = np.array(img_pil)
        imgs = [np.array(img_pil_) for img_pil_ in img_pils]

        # Calculating 128 dim encoding of the face in the image
        face_image_encoding = face_recognition.face_encodings(img)[0]
        face_image_encodings = [face_recognition.face_encodings(img_)[0] for img_ in imgs]

        # Calculating distance (D) between face image encodings, Probability of face match = 1 - D 
        results = 1 - face_recognition.face_distance(face_image_encodings, face_image_encoding)
        
        # Sorting the probabilites for comparing Faces in the database
        sorted_index = sorted(range(len(results)), key=lambda k: results[k])
        length = 3 if len(results) > 2 else len(results)
        probability = [results[sorted_index[i-1]] for i in range(len(results), len(results) - length, -1)] # sorted top probabities

        # Converting image to base64 encoded string 
        img_str = self.img2str(img_pil)
        img_strs = [ self.img2str(img_pils[sorted_index[i-1]]) for i in range(len(results), len(results) - length, -1)]
        indices = sorted_index[-length:]
        return probability, img_str, img_strs, indices

    def num_faces(self, image, model = 'hog'):
        """
        Function : for computing number of faces in the image
        Input    : image  -> image
                   model  -> 'hog' or 'cnn'
        Output   : num_faces -> integer
        """
        # Image in bytes format
        image  = io.BytesIO(image)

        # Bytes to PIL Image to numpy array
        img = np.array(Image.open(image))

        # Computing location of the face in the image
        face_locations = face_recognition.face_locations(img, model = model)
        num_faces = len(face_locations)
        return num_faces
    
    def facial_landmarks(self, image):
        """
        Function : for computing features of face in the image
        Input    : image  -> image
        Output   : img_str -> Modified image with features encoded as base64 string
        """

        # Image in bytes format
        image  = io.BytesIO(image)
        # Bytes to PIL Image 
        img_pil = Image.open(image)
        # PIL image to numpy array
        img = np.array(img_pil)

        # Computing facial features such as chin, nose, eyebrows, upperlip, lower lip, jawline        
        landmarks = face_recognition.face_landmarks(img)

        # Drawing features onto the image
        draw = ImageDraw.Draw(img_pil)
        for key in landmarks[0].keys():
            locations = landmarks[0][key]
            for loc in locations:
                r= 5
                draw.ellipse((loc[0]-r, loc[1]-r, loc[0]+r, loc[1]+r), fill='red')
        
        # Converting image to base64 encoded string 
        img_str = self.img2str(img_pil)
        return img_str
    
    def img2str(self, img):
        """
        Function : for converting PIL image to Base64 encoded string
        Input    : image  ->  PIL Image
        Output   : img_str -> Modified image with features encoded as base64 string
        """
        buffered = io.BytesIO()
        img.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue()).decode('UTF-8')
        return img_str
        
