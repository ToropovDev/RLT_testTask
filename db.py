import os
import pymongo
from datetime import datetime

db_client = pymongo.MongoClient("mongodb://localhost:27017/")
database = db_client["payments_db"]
collection = database["sample_collection"]


def start_db():
    if collection.count_documents(filter={}) == 0:
        os.popen("mongorestore -d payments_db dump/sampleDB/sample_collection.bson")


def get_response(request):
    group_type = request["group_type"]
    match group_type:
        case "hour":
            pass
        case "day":
            pass
        case "week":
            pass
        case "month":
            return get_response_month(request)


def get_response_month(request):
    dt_from = datetime.fromisoformat(request["dt_from"])
    dt_upto = datetime.fromisoformat(request["dt_upto"])
    data = []

    for item in collection.find(
        filter={"dt": {"$gte": dt_from, "$lte": dt_upto}},
    ):
        data.append({
            'dt': item['dt'].replace(day=1, hour=0, minute=0, second=0).isoformat(),
            'value': item['value']
        })

    data_dict = {}
    for item in data:
        date_str = item['dt']
        if item['dt'] not in data_dict.keys():
            data_dict[date_str] = item['value']
        else:
            data_dict[date_str] += item['value']

    result = {
        "dataset": list(data_dict.values()),
        "labels": list(data_dict.keys()),
    }
    return result


