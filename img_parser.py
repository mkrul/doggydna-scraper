import os
import pdb as p
from PIL import Image
from pytesseract import pytesseract as pt
import shutil

pt.tesseract_cmd = r'/usr/local/bin/tesseract'

def remove_non_conforming_images():
  directories = os.listdir("images")
  for dir in directories:
    for filename in os.listdir(f"images/{dir}"):
      file_count = len(os.listdir(f"images/{dir}"))
      image = Image.open(f"images/{dir}/{filename}")
      text = pt.image_to_string(image)
      if "%" in text:
        print(text)
        break
      else:
        if file_count == os.listdir(f"images/{dir}").index(filename) + 1:
          shutil.rmtree(f"images/{dir}")
          print(f"Removed {dir}")
        else:
          continue

remove_non_conforming_images()