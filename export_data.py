import os
import pdb as p
import sys
from PIL import Image
import cv2
from pytesseract import pytesseract as pt
import json
import subprocess

pt.tesseract_cmd = r'/usr/local/bin/tesseract'

def find_breed_data():
  results = {}
  directories = os.listdir("images")
  num_dirs = len(directories)
  iterator = 1
  with open("results.json", "w") as infile:
    for dir in directories:
      try:
        results[directories.index(dir)] = {
          "images": [],
          "breeds": {
            "src": [],
            "data": {}
          }
        }
        print(f"Processing {iterator}/{num_dirs}: {dir}")
        iterator += 1
        for filename in os.listdir(f"images/{dir}"):
          image = Image.open(f"images/{dir}/{filename}")
          text = pt.image_to_string(image)
          if text != "":
            print("Found breed data")
            results[directories.index(dir)]["breeds"]["src"].append(f"images/{dir}/{filename}")
          else:
            print("Found dog image")
            results[directories.index(dir)]["images"].append(f"images/{dir}/{filename}")
      except:
        print("Error")
        continue
    json.dump(results, infile)

# def process_breed_data():
#   breed_data = {}
#   results = find_breed_data()

#   with open("results.json", "w") as infile:
#     for each in results:
#       print(f"Processing {results[each]['breeds']['src']}")
#       add_breed = 'y'
#       while add_breed == 'y':
#         breed = input("Breed name: ")
#         percentage = input("Percentage: ")
#         breed_data[breed] = percentage
#         results[each]["breeds"]["data"] = breed_data
#         add_breed = input("Add another breed? (y/n) ")

#       json.dump(results, infile)

find_breed_data()