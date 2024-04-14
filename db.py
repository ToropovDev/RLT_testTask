import os
import pymongo
from datetime import datetime, timedelta
import pandas as pd
from config import MONGO_URL, DATABASE_NAME

db_client = pymongo.MongoClient(MONGO_URL)
database = db_client[DATABASE_NAME]
collection = database["sample_collection"]


def start_db() -> None:
    if collection.count_documents(filter={}) == 0:
        os.popen("mongorestore -d payments_db dump/sampleDB/sample_collection.bson")


def group_by_hour(dt_from: datetime, dt_upto: datetime) -> dict:
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


def group_by_day(dt_from: datetime, dt_upto: datetime) -> dict:
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


def process_weekday(date: str) -> datetime:
    date = datetime.fromisoformat(date)
    if date.weekday() == 0:
        return date
    if date.weekday() == 1:
        return date - timedelta(days=1)
    if date.weekday() == 2:
        return date - timedelta(days=2)
    if date.weekday() == 3:
        return date - timedelta(days=3)
    if date.weekday() == 4:
        return date - timedelta(days=4)
    if date.weekday() == 5:
        return date - timedelta(days=5)
    if date.weekday() == 6:
        return date - timedelta(days=6)


def group_by_week(dt_from: datetime, dt_upto: datetime) -> dict:
    data_dict = {}
    dates = pd.date_range(dt_from, dt_upto, freq="W")
    for date in dates:
        date = process_weekday(str(date))
        data_dict[date.isoformat()] = 0
    for item in collection.find(
            filter={"dt": {"$gte": dt_from, "$lte": dt_upto}},
        ):
        new_dt = item['dt'].replace(day=1, hour=0, minute=0, second=0).isoformat()
        new_dt = process_weekday(new_dt).isoformat()
        data_dict[new_dt] += item['value']
    return data_dict


def group_by_month(dt_from: datetime, dt_upto: datetime) -> dict:
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


def get_response(request: dict) -> str:
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

