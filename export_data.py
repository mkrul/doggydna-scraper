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
  for dir in directories:
    results[directories.index(dir)] = {
      "images": [],
      "breeds": {
        "src": [],
        "data": {}
      }
    }
    print(f"Processing {dir}")
    for filename in os.listdir(f"images/{dir}"):
      image = Image.open(f"images/{dir}/{filename}")
      text = pt.image_to_string(image)
      if "%" in text:
        print("Found breed data")
        results[directories.index(dir)]["breeds"]["src"].append(f"images/{dir}/{filename}")
      else:
        print("Found dog image")
        results[directories.index(dir)]["images"].append(f"images/{dir}/{filename}")

    break
  return results

def process_breed_data():
  breed_data = {}
  results = find_breed_data()

  display_breed_data(results)

  with open("results.json", "w") as infile:
    for each in results:
      add_breed = 'y'
      while add_breed == 'y':
        breed = input("Breed name: ")
        percentage = input("Percentage: ")
        breed_data[breed] = percentage
        results[each]["breeds"]["data"] = breed_data
        add_breed = input("Add another breed? (y/n) ")

    json.dump(results, infile)

def display_breed_data(results):
  subprocess.run(['python3', 'display_breed_data.py', '--results', str(results)])

process_breed_data()