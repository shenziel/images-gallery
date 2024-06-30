import os
from pymongo import MongoClient
from dotenv import dotenv_values

config = {
    **os.environ,  # override loaded values with environment variables
    **dotenv_values(".env.local"),
}

MONGO_URL = config.get("MONGO_URL", "mongo")
MONGO_USERNAME = config.get("MONGO_USERNAME", "root")
MONGO_PASSWORD = config.get("MONGO_PASSWORD", "")
MONGO_PORT = config.get("MONGO_PORT", 27017)

mongo_client = MongoClient(
    host=MONGO_URL,
    username=MONGO_USERNAME,
    password=MONGO_PASSWORD,
    port=MONGO_PORT,
)


def insert_test_document():
    """inserts sample document to the test_collection in the test db"""
    db = mongo_client.test
    test_collection = db.test_collection
    res = test_collection.insert_one({"name": "Pedro", "instructor": False})
    print(res)
