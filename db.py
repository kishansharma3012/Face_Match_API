# Face Match API By @Kishan
# db.py -->  Database for storing images (Redis, Sqlite3)

# Importing libraries
import sqlite3
import redis
from os import path, getcwd

# Class Database_Redis : Redis based database for storing images and user names
class Database_Redis:
    
    def __init__(self):
        """
        Function : for initializing connection to database server
        """
        self.connection = redis.Redis() 

    def insert(self, key, image, name):
        """
        Function : for inserting image with user name at UUID as key in the database
        Input    : key  -> UUID
                   image -> image file
                   name -> user name
        Output   : result -> Key (Success) or 0 (Error)
        """
        try:
            # Entering key to value with hash name
            self.connection.hset(str(key), "imagefile", image)
            self.connection.hset(str(key), "user_name", name)
            result = key
        except:
            print('DB INSERT ERROR !!')
            result = 0
        return result

    def select(self, key):
        """
        Function : for finding image and user name using key in the database
        Input    : key  -> UUID
        Output   : result -> image (Success) or 0 (Error)
                   username -> user name string (Success) or None (Error)
        """
        # Checking if key exist in the database
        if self.connection.exists(key):
            result = self.connection.hget(key, "imagefile")
            username = self.connection.hget(key, "user_name")
        else:
            print('DB SELECT Error!!')
            result = 0 
            username = None
        return result, username


    def delete(self, key):
        """
        Function : for Deleting image and user name using key in the database
        Input    : key  -> UUID
        Output   : result -> 1 (Success) or 0 (Error)
        """
        # Checking if key exist in the database
        if self.connection.exists(key):
            result = self.connection.delete(key)
        else:
            print('DB DELETE: UUID Does not exist')
            result = 0 
            
        return result

# Class Database_Sqlite : Sqlite based database for storing images and user names
class Database_Sqlite:

    def __init__(self):
        """
        Function : for initializing connection to database server
        """
        db = path.join(getcwd(), 'face_database.db')
        self.connection = sqlite3.connect(db, check_same_thread=False)

    def query(self, q, arg=()):
        """
        Function : for finding image with user name at UUID as key in the database
        Input    : q  -> query
                   arg -> arguments (UUID)
        Output   : result -> image file and user name (Success) or 0 (Error)
        """
        cursor = self.connection.cursor()
        cursor.execute(q, arg)
        results = cursor.fetchall()
        cursor.close()
        return results

    def insert(self, q, arg=()):
        """
        Function : for inserting image with  UUID as key in the database
        Input    : q  -> query
                   arg ->arguments (key and image file)
        Output   : result -> id (Success) or None (Error)
        """
        
        cursor = self.connection.cursor()
        cursor.execute(q, arg)
        self.connection.commit()
        result = cursor.lastrowid
        cursor.close()
        return result

    def select(self, q, arg=()):
        """
        Function : for selecting image with user name at UUID as key in the database
        Input    : q  -> query
                   arg -> arguments (UUID)
        Output   : result -> image file and user name (Success) or 0 (Error)
        """
        cursor = self.connection.cursor()
        return cursor.execute(q, arg)

    def delete(self, q, arg=()):
        """
        Function : for Deleting image using key in the database
        Input    : q  -> query
                   arg -> arguments (UUID)
        Output   : result -> 1 (Success) or 0 (Error)
        """
        cursor = self.connection.cursor()
        result = cursor.execute(q, arg)
        self.connection.commit()
        return result