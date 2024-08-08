import config
from pymongo import MongoClient
import os
import sys

client = MongoClient(f"mongodb+srv://{config.mongo_user}:{config.mongo_senha}@mongo-fiap-food-936cf8b1.mongo.ondigitalocean.com/")
db = client[config.mongo_db]
collection = db.get_collection(config.mongo_collection)

faturas = collection.find_one({"id_fatura": 3})

print(faturas)