from pymongo import MongoClient
import praw
import os
import pdb as p
import requests
from PIL import Image
from imgurpython import ImgurClient

def get_database():
  client = MongoClient(os.environ["MONGO_DB_URI"])
  return client.get_default_database()

db = get_database()
collection = db["dogs"]

reddit = praw.Reddit(
  client_id=os.environ["REDDIT_CLIENT_ID"],
  client_secret=os.environ["REDDIT_CLIENT_SECRET"],
  password=os.environ["REDDIT_PASSWORD"],
  user_agent=os.environ["REDDIT_USER_AGENT"],
  username=os.environ["REDDIT_USERNAME"],
)

subreddit = reddit.subreddit("doggydna")
image_iterator = 0
sizes = []

if not os.path.exists(f"images/"):
  os.mkdir(f"images/")

for submission in subreddit.new(limit=10):
  try:
    if submission.media_metadata:
      items = submission.media_metadata.items()
      if len(items) > 3:
        if not os.path.exists(f"images/{submission.id}"):
          os.mkdir(f"images/{submission.id}")

          for key, value in items:

            if value["e"] == "Image":
              for image_data in value["p"]:
                size = image_data["y"]
                sizes.append(size)

              for image_data in value["p"]:
                if image_data["y"] == max(sizes):
                  url = image_data["u"]
                  image = Image.open(requests.get(url, stream=True).raw)
                  image.save(f"images/{submission.id}/{image_iterator}.jpg")
                  image_iterator += 1
                  sizes = []

      image_iterator = 0

  except Exception as e:
    print(e)
    continue
