from pymongo import MongoClient

import config.settings as settings

client = MongoClient(settings.MONGO_URL)
db = client.test

