
import os
import dotenv

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

dotenv.load_dotenv()

if os.getenv("ENV") == "prod":
    username = os.getenv('MONGO_DB_USERNAME')
    password = os.getenv('MONGO_DB_PASSWORD')

    uri = f"mongodb+srv://{username}:{password}@cluster0.n4hegjm.mongodb.net/?retryWrites=true&w=majority"

    # Create a new client and connect to the server
    client = MongoClient(uri, server_api=ServerApi('1'))

    database =  client["chat_history_database"]
    collection = database["ccl_collection"]
else:
    collection = MongoClient('localhost', 27017)["testdb"]["test_collection"]
