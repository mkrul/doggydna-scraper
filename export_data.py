import os
import pdb as p
import sys
from PIL import Image
import cv2
from pytesseract import pytesseract as pt
import json
import shutil
import subprocess

pt.tesseract_cmd = r'/usr/local/bin/tesseract'

def find_breed_data():
  results = {}
  directories = os.listdir("images")
  num_dirs = len(directories)
  iterator = 1
  with open("results.json", "w") as infile:
    for dir in directories:
      # if no images exist
      try:
        if len(os.listdir(f"images/{dir}")) <= 2:
          print(f"Invalid number of images for {dir}")
          shutil.rmtree(f"images/{dir}")
          continue
        results[directories.index(dir)] = {
          "images": [],
          "data": {
            "breeds": [],
          }
        }
        print(f"Processing {iterator}/{num_dirs}: {dir}")
        iterator += 1
        for filename in os.listdir(f"images/{dir}"):
          image = Image.open(f"images/{dir}/{filename}")
          text = pt.image_to_string(image)
          if text == "":
            print("Found dog image")
            results[directories.index(dir)]["images"].append(f"images/{dir}/{filename}")
      except:
        print("Error")
        continue
    json.dump(results, infile)

find_breed_data()