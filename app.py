import pymongo
import dotenv
import os
from pprint import pprint
import datetime

dotenv.load_dotenv()

MONGODB_URL = os.environ["MONGODB_URL"]

client = pymongo.MongoClient(MONGODB_URL, serverSelectionTimeoutMS=5000)

db = client['sample_weatherdata']
data = db['data']

pprint(data.find_one({"ts": datetime.datetime(1984, 3, 5, 18, 0)}))
