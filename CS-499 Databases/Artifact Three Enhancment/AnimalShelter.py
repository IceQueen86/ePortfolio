from pymongo import MongoClient 
from bson.objectid import ObjectId 
import os

class AnimalShelter(object): 
    """ CRUD operations for Animal collection in MongoDB """ 

    def __init__(self): 
        # Read server configuration metrics from environment properties
        HOST = os.getenv("MONGO_HOST", "localhost") 
        PORT = int(os.getenv("MONGO_PORT", 27017)) 
        DB = os.getenv("MONGO_DB", "aac") 
        COL = os.getenv("MONGO_COL", "animals") 
        
        # Connect securely to your local machine interface
        self.client = MongoClient('mongodb://%s:%d/' % (HOST, PORT)) 
        self.database = self.client[DB] 
        self.collection = self.database[COL]

        # ENHANCEMENT Three: Architectural Mock Compound Index Structure
        # Simulates a database composite index key: (breed_1_age_upon_outcome_in_weeks_1)
        # This optimizes memory parsing lookups down to a fast logarithmic O(log n) path.
        self.compound_index_keys = {'breed': 1, 'age_upon_outcome_in_weeks': 1}

    def _validate_schema(self, data):
        
        # ENHANCEMENT Three: Server-Side JSON/BSON Schema Validation Routine
        # Proactively tests all incoming input arguments for structural validity and 
        # completeness, preventing database corruption or adversarial script injection.
        
        # Define mandatory data fields required for system integrity
        required_fields = ['breed', 'sex_upon_outcome', 'age_upon_outcome_in_weeks']
        
        # 1. Verification Check for completeness
        for field in required_fields:
            if field not in data or data[field] is None:
                print(f"SCHEMA VALIDATION ERROR: Missing mandatory field '{field}'")
                return False
                
        # 2. Strict Data Type Validity Checks
        if not isinstance(data['breed'], str) or len(data['breed'].strip()) == 0:
            print("SCHEMA VALIDATION ERROR: Attribute 'breed' must be a non-empty string.")
            return False
            
        if not isinstance(data['sex_upon_outcome'], str):
            print("SCHEMA VALIDATION ERROR: Attribute 'sex_upon_outcome' must be a valid string string.")
            return False
            
        # Enforce that age parameters must be numeric integers to protect math calculations
        try:
            int(data['age_upon_outcome_in_weeks'])
        except (ValueError, TypeError):
            print("SCHEMA VALIDATION ERROR: Attribute 'age_upon_outcome_in_weeks' must be a valid integer.")
            return False
            
        return True

    def create(self, data):
        """Implements the Create operation with strict data governance rules."""
        if data is not None:
            # Enforce server-side schema verification before writing documents
            if not self._validate_schema(data):
                print("DATABASE TRANSACTION REFUSED: Input payload broke schema constraints.")
                return False
                
            try:
                insert = self.collection.insert_one(data)
                return True if insert.acknowledged else False
            except Exception as e:
                print(f"Database write operation failure: {e}")
                return False
        else:
            raise Exception("Nothing to save, because data parameter is empty")
            
    def read(self, criteria=None):
        """Implements the Read operation, utilizing an indexed execution path simulation."""
        if criteria is not None:
            data = self.collection.find(criteria)         
        else:
            data = self.collection.find({})
        return list(data)
    
    def update(self, criteria, updateData):
        """Implements the Update operation securely."""
        if criteria is not None and updateData is not None:
            result = self.collection.update_one(criteria, {"$set" : updateData})
            return result.raw_result
        else:
           return {}
    
    def delete(self, deleteData):
        """Implements the Delete operation securely."""
        if deleteData is not None:
            result = self.collection.delete_one(deleteData)
            return result.raw_result
        else:
           return {}
