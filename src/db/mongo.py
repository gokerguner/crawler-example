import sys
import pymongo
from pymongo import MongoClient
from config.envparams import Params
from pymongo.errors import AutoReconnect
import time
import os
import urllib


PARAM_FILE_PATH = "./params.json"
prms = Params(param_file_path=PARAM_FILE_PATH)

host = os.environ["mongo_host"]
port = os.environ["mongo_port"]
database = os.environ["mongo_database"]
user = urllib.parse.quote(os.environ["mongo_user"])
password = urllib.parse.quote(os.environ["mongo_password"])
auth_db = os.environ["auth_db"]
host_string = "mongodb://{}:{}@{}:{}/{}?authSource={}".format(user, password,
                                                                 host, port, database, auth_db)

def connect2db(host, port, maxservdelay, logging=None):
    _client = None
    retry_count = 0
    while retry_count < 10:
        try:
            _client = MongoClient(host_string)
            logging.info(host_string)
            time.sleep(1)
            _client.server_info()
            logging.info(f"Connected to Mongodb server.")
            break
        except (pymongo.errors.ServerSelectionTimeoutError, pymongo.errors.AutoReconnect) as err:
            logging.error(f"{err}. Mongodb Connection Error! I'll try again and again until I reach the success. Waiting for {pow(2, retry_count)} secs.")
            time.sleep(pow(2, retry_count))
            retry_count += 1
    if _client is None:  # guarantee quitting..
        logging.fatal("Cannot create mongoclient to db! quitting...")
        sys.exit(1)
    return _client


def getDb(client, DB_NAME, logging=None):

    _db = client[DB_NAME]
    return _db


def createIndexes(client, prms, logging=None):
    db = getDb(client, database, logging=logging)
    ##hepsiburada
    _result = db[prms.DB_HEPSIBURADA_COLLECTION].create_index('id', unique=True)
    logging.debug("Unique index param set as <id> for collection:{collection} : {status}".format(
        collection=prms.DB_HEPSIBURADA_COLLECTION,
        status=_result))
    ##hepsiburada_comments
    _result = db[prms.DB_HEPSIBURADA_COMMENTS_COLLECTION].create_index('product_id', unique=True)
    logging.debug("Unique index param set as <id> for collection:{collection} : {status}".format(
        collection=prms.DB_HEPSIBURADA_COLLECTION,
        status=_result))


