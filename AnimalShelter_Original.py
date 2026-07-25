# Example Python Code to Insert a Document 

from pymongo import MongoClient 
from bson.objectid import ObjectId 

class AnimalShelter(object): 
    """ CRUD operations for Animal collection in MongoDB """ 

    def __init__(self): 
        # Initializing the MongoClient. This helps to access the MongoDB 
        # databases and collections. This is hard-wired to use the aac 
        # database, the animals collection, and the aac user. 
        # 
        # You must edit the password below for your environment. 
        # 
        # Connection Variables 
        # 
        USER = 'aacuser' 
        PASS = 'slodoz96' 
        HOST = 'localhost' 
        PORT = 27017 
        DB = 'aac' 
        COL = 'animals' 
        # 
        # Initialize Connection 
        # 
        self.client = MongoClient('mongodb://%s:%s@%s:%d' % ("aacuser","slodoz96","localhost",27017)) 
        self.database = self.client['%s' % (DB)] 
        self.collection = self.database['%s' % (COL)]

    # Create a method to return the next available record number for use in the create method
            
    # Complete this create method to implement the C in CRUD. 
    def create(self, data):
        if data is not None:
            insert = self.database.animals.insert_one(data)  # data should be dictionary
            # Check insert for operation
            if insert!=0:
                return True
            else:
                # Default return
                return False    
        else:
            raise Exception("Nothing to save, because data parameter is empty")
            
    # Create method to implement the R in CRUD.
    def read(self, criteria=None):
        if criteria is not None:
            data = self.database.animals.find(criteria)         
        else:
            data = self.database.animals.find({})
        # Return the dataset else let the error flow up
        return data
    
    # Create method to implement the U in CRUD.
    def update(self, criteria, updateData):
        if criteria is not None:
            result = self.database.animals.update_one(criteria, {"$set" : updateData})
        else:
           return"{}"
        return result.raw_result
    
    # Create method to implement the D in CRUD.
    def delete(self, deleteData):
        if deleteData is not None:
            result = self.database.animals.delete_one(deleteData)
        else:
           return"{}"
        return result.raw_result
        
        
        

            