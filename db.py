import os
import pymongo
from datetime import datetime

db_client = pymongo.MongoClient("mongodb://localhost:27017/")
database = db_client["payments_db"]
collection = database["p"]


def start_db():
    if collection.count_documents(filter={}) == 0:
        os.popen("mongorestore -d payments_db dump/sampleDB/sample_collection.bson")


def get_response(request):
    response = {"dataset": [],
                "labels": []}
