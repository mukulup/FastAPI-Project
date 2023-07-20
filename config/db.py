import datetime
import logging
from bson import ObjectId
from pymongo import MongoClient

import config.settings as settings
from utils import *
client = MongoClient(settings.MONGO_URL)
database = client.test


def clean(query):
    if query and query.get("_id"):
        if type(query.get("_id")) == dict:
            op = list(query.get("_id").keys())[0]
            val = query.get("_id")[op]
            if type(val) == list:
                val = [ObjectId(id) for id in val]
            else:
                val = ObjectId(val)
            query["_id"] = {op: val}
        else:
            query.update({"_id": ObjectId(query.get("_id"))})
    return query


def create_values(values):
    query =  None
    if values:
        query = {k: 1 for k in values}
    return query

def _sort(data=None):
    if not data:
        return ("_id", 1)
    return data


def timestamp(data, update=False):
    current_time = datetime.now()
    timezone_name = current_time.astimezone().tzname()
    if timezone_name != 'UTC':
        current_time = current_time.astimezone(pytz.utc).replace(tzinfo=None)
    timestamp_dict = {'modified_at': current_time}
    if not update:
        timestamp_dict['created_at'] = current_time
    if isinstance(data, list):
        for d in data:
            d.update(timestamp_dict)
    else:
        data.update(timestamp_dict)
    return data


class DB():

    @classmethod
    async def create(cls, data={}):
        try:
            if data:
                data = timestamp(data)
                db_document = await database[cls.__name__.lower()].insert_one(data)
                return {"_id": str(db_document.inserted_id)}
            else:
                return {"_id": None}
        except Exception as error:
            logging.exception(f"Error while writing to collection {cls.__name__.lower()}, with error {error}, "
                              f"for data {data}")
            
    @classmethod
    async def get(cls, query={}, values = []):
        try:
            db_document = await database[cls.__name__.lower()].find_one(clean(query), create_values(values))
            return db_document
        except Exception as e:
            logging.info(f"Error while getting value from collection {cls.__name__.lower()}, Error occured: {str(e)}")

    @classmethod
    async def filter(cls, query={}, values=[], order_by=None, paginate=(0,0)):
        try:
            _order = _sort(order_by)
            start, end = paginate
            db_document = await database[cls.__name__.lower()].find(clean(query), create_values(values)).skip(start).limit(end).sort(_order[0], _order[1]).to_list(110000000)  #
            if(values and db_document):
                if "_id" in db_document[0]:
                    for dt in db_document:
                        dt['_id'] = str(dt['_id'])
                return db_document
            return objectsList(cls.object, db_document)
        except Exception as error:
            logging.exception(f"[{error}]")

    @classmethod
    async def update(cls, id, data, upsert: bool = False):
        try:
            if data and id and type(data) == dict:
                data = timestamp(data, update=True)
                db_document = await database[cls.__name__.lower()].update_one(clean(id), {"$set": data}, upsert=upsert)
                return db_document.acknowledged
            elif data and id and type(data) == list:
                data = timestamp(data, update=True)
                db_document = await database[cls.__name__.lower()].update_one(clean(id), {"$push": data}, upsert=upsert)
                return db_document.acknowledged
            else:
                return False
        except Exception as error:
            logging.exception(f"[{error}]")
    
    @classmethod
    async def paginate(cls, query={},values=[], order_by=("_id", settings.DESC), page_no=1, page_size=10):
        _order = _sort(order_by)
        total_records = await database[cls.__name__.lower()].count_documents(clean(query))
        data = []
        if total_records > 0:
            skip = (page_no-1) * page_size
            limit = page_size
            data = await database[cls.__name__.lower()].find(clean(query),create_values(values)).skip(skip).limit(limit).sort(_order[0], _order[1]).to_list(110000000)
            if not values:
                data = objectsList(cls.object, data)
            else:
                for d in data:
                    d['_id'] = str(d['_id'])
        return paginate_data(total_records, data, page_no, page_size)