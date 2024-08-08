import config
from pymongo import MongoClient
import os
import sys

class db_mongo_class:
    def __init__(self):

        # Configurações do banco de dados
        self.client = MongoClient(f"mongodb+srv://{config.mongo_user}:{config.mongo_senha}@mongo-fiap-food-936cf8b1.mongo.ondigitalocean.com/")
        


    def get_collection(self):
        self.db = self.client[config.mongo_db]
        collection = self.db.get_collection(config.mongo_collection)
        return collection


