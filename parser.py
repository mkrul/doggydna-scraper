from pymongo import MongoClient
import praw
import os
import pdb as p
import requests
from PIL import Image
from queue import Queue
from threading import Thread
import multiprocessing

NUM_THREADS = 5

def get_database():
  client = MongoClient(os.environ["MONGO_DB_URI"])
  return client.get_default_database()

def connect_to_collection():
  db = get_database()
  return db["dogs"]

def parse_image_data():
    for filename in os.listdir("images/19etch4"):
      if filename.endswith(".jpg"):
        with open(f"images/19etch4/{filename}", "rb") as image_file:
          f = open("results.json", "a")
          image = image_file.read()
          data = {
            "image": image,
          }
          f.write(str(data))

if __name__ == '__main__':

  jobs = []

  for i in range(NUM_THREADS):
    process = multiprocessing.Process(target=parse_image_data)

    jobs.append(process)

  for j in jobs:
    j.start()

  for j in jobs:
    j.join()



