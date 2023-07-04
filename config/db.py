import logging
from pymongo import MongoClient

import config.settings as settings

client = MongoClient(settings.MONGO_URL)
database = client.test

class DB():

    @classmethod
    async def create(cls, data={}):
        try:
            if data:
                db_document = await database[cls.__name__.lower()].insert_one(data)
                return {"_id": str(db_document.inserted_id)}
            else:
                return {"_id": None}
        except Exception as error:
            logging.exception(f"Error while writing to collection {cls.__name__.lower()}, with error {error}, "
                              f"for data {data}")
            
    @classmethod
    async def get(cls, query={}):
        try:
            db_document = await database[cls.__name__.lower()].find_one(query)
            return db_document
        except Exception as e:
            logging.info(f"Error while getting value from collection {cls.__name__.lower()}, Error occured: {str(e)}")

    @classmethod
    async def filter(cls, query):
        try:
            db_document = await database[cls.__name__.lower()].find(query)

            if db_document:
                return db_document
            else:
                return {}
        except Exception as e:
            logging.info(f"Error while getting value from collection {cls.__name__.lower()}, Error occured: {str(e)}")