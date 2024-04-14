import os
import pymongo
from datetime import datetime
import pandas as pd

db_client = pymongo.MongoClient("mongodb://localhost:27017/")
database = db_client["payments_db"]
collection = database["sample_collection"]


def start_db():
    if collection.count_documents(filter={}) == 0:
        os.popen("mongorestore -d payments_db dump/sampleDB/sample_collection.bson")


def group_by_hour(dt_from, dt_upto):
    data_dict = {}
    dates = pd.date_range(dt_from, dt_upto, freq="h")
    for date in dates:
        data_dict[date.isoformat()] = 0
    for item in collection.find(
            filter={"dt": {"$gte": dt_from, "$lte": dt_upto}},
    ):
        new_dt = item['dt'].replace(minute=0, second=0).isoformat()
        data_dict[new_dt] += item['value']
    return data_dict


def group_by_day(dt_from, dt_upto):
    data_dict = {}
    dates = pd.date_range(dt_from, dt_upto, freq="D")
    for date in dates:
        data_dict[date.isoformat()] = 0
    for item in collection.find(
            filter={"dt": {"$gte": dt_from, "$lte": dt_upto}},
    ):
        new_dt = item['dt'].replace(hour=0, minute=0, second=0).isoformat()
        data_dict[new_dt] += item['value']
    return data_dict


def group_by_week(dt_from, dt_upto):
    pass


def group_by_month(dt_from, dt_upto):
    data_dict = {}
    dates = pd.date_range(dt_from, dt_upto, freq="MS")
    for date in dates:
        data_dict[date.isoformat()] = 0
    for item in collection.find(
        filter={"dt": {"$gte": dt_from, "$lte": dt_upto}},
    ):
        new_dt = item['dt'].replace(day=1, hour=0, minute=0, second=0).isoformat()
        data_dict[new_dt] += item['value']
    return data_dict


def get_response(request):
    dt_from = datetime.fromisoformat(request["dt_from"])
    dt_upto = datetime.fromisoformat(request["dt_upto"])
    group_type = request["group_type"]

    data_dict = {}
    match group_type:
        case "hour":
            data_dict = group_by_hour(dt_from, dt_upto)
        case "day":
            data_dict = group_by_day(dt_from, dt_upto)
        case "week":
            data_dict = group_by_week(dt_from, dt_upto)
        case "month":
            data_dict = group_by_month(dt_from, dt_upto)

    result = {
        "dataset": list(data_dict.values()),
        "labels": list(data_dict.keys()),
    }
    result = str(result).replace("'", '"')
    return result

