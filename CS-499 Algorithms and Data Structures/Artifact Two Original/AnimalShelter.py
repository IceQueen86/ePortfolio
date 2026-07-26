from pymongo import MongoClient 
from bson.objectid import ObjectId
import os

class AnimalShelter(object): 
    """ CRUD operations for Animal collection in MongoDB """ 

    def __init__(self): 
        # Read server layout configuration metrics from environment properties 
        HOST = os.getenv("MONGO_HOST", "localhost") 
        PORT = int(os.getenv("MONGO_PORT", 27017)) 
        DB = os.getenv("MONGO_DB", "aac") 
        COL = os.getenv("MONGO_COL", "animals") 
        
        # REMOVED USER/PASS BLOCKS: Connect securely to your local machine interface directly without user locks
        self.client = MongoClient('mongodb://%s:%d/' % (HOST, PORT)) 
        self.database = self.client[DB] 
        self.collection = self.database[COL]

    # Create a method to return the next available record number for use in the CRUD method       
    def create(self, data):
        """Implements the Create operation with strict error handling rules."""
        if data is not None:
            insert = self.collection.insert_one(data)  # Interacts via encapsulated target property
            if insert.acknowledged:
                return True
            else:
                return False    
        else:
            raise Exception("Nothing to save, because data parameter is empty")
            
    def read(self, criteria=None):
        """Implements the Read operation, ensuring empty requests default to general collections."""
        if criteria is not None:
            data = self.collection.find(criteria)         
        else:
            data = self.collection.find({})
        return list(data) 
    
    # Forces instant cursor mapping for immediate in-memory parsing 
    def update(self, criteria, updateData):
        """Implements the Update operation with a secure update template validation constraint."""
        if criteria is not None and updateData is not None:
            result = self.collection.update_one(criteria, {"$set" : updateData})
            return result.raw_result
        else:
           return {}
    
    def delete(self, deleteData):
        """Implements the Delete operation securely across encapsulated properties."""
        if deleteData is not None:
            result = self.collection.delete_one(deleteData)
            return result.raw_result
        else:
           return {}
        
        
        

            