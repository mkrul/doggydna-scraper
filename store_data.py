import json
from pymongo import MongoClient
import os

def get_database():
  client = MongoClient(os.environ["MONGO_DB_URI"])
  return client.get_default_database()

def store_data():
  db = get_database()
  collection = db["dogs"]

  # read data from temp_results.json
  with open("temp_results.json", "r") as infile:
    data = json.load(infile)

  # insert data into database
  for key, value in data.items():
    print(key, value)
    collection.insert_one(value)

store_data()