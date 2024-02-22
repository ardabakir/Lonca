#database connection class
import datetime
from pymongo import MongoClient

class Database:
    def __init__(self):
        self.CONNECTION_STRING = "mongodb://root:example@localhost/lonca?authSource=admin&retryWrites=true&w=majority"
        self.client = MongoClient(self.CONNECTION_STRING)
        self.db = self.client['local']

    def upsert_data(self, data):
        now = datetime.datetime.now()
        self.db.products.update_one(data,update={'$setOnInsert':{'createdAt':now,},'$set':{'updatedAt':now,},}, upsert=True)

    def get_database(self):
        return self.db

    def upsert_many(self, data):
        now = datetime.datetime.now()
        for item in data:
            self.db.products.update_one(item,update={'$setOnInsert':{'createdAt':now,},'$set':{'updatedAt':now,},}, upsert=True)

    def close_connection(self):
        self.client.close()