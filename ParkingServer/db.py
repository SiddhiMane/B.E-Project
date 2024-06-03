from sqlitedict import SqliteDict
from constants import Constants

class Database:

    def __init__(self) -> None:
        try:
            self.myDb = SqliteDict(Constants.DATABASE_NAME, autocommit=True)
        except Exception as err:
            print(f"An exception has occured while creating database file. Hint: {err}")
    
    def __del__(self):
        try:
            self.myDb.close()
        except Exception as err:
            print(f"An exception has occured while closing database file. Hint: {err}")
            
    def exists(self, key):
        try:
            return key in self.myDb
        except Exception as err:
            print(f"An exception has occurred while checking key existence. Hint: {err}")
            return False

    def insert(self, key, value):
        try:
            if self.exists(key):
                print("This Information is already inserted")
                return False
            self.myDb[key] = value
            return True
        except Exception as err:
            print(f"An exception has occured while inserting values into database. Hint: {err}")
            return False

    def get(self, key):
        try:
            if not self.exists(key):
                return False
            return self.myDb[key]
        except Exception as err:
            print(f"An exception has occured while reading values from database. Hint: {err}")
            return False
    
    def getAllValues(self):
        try:
            return list(self.myDb.values())
        except Exception as err:
            print(f"An exception has occured while reading all values from database. Hint: {err}")
            return False
    
    def set(self, key, slots):
        try:
            if not self.exists(key):
                print("Information does not exists or is invalid.")
                return False
            doc = self.get(key)
            doc["available_slots"] = slots
            self.myDb[key] = doc
            return True
        except Exception as err:
            print(f"An exception has occured while updating values into database. Hint: {err}")
            return False
    
    def remove(self, key):
        try:
            if not self.exists(key):
                print("Information does not exists or is invalid.")
                return False
            del self.myDb[key]
            return True
        except Exception as err:
            print(f"An exception has occured while deleting values from database. Hint: {err}")
            return False
