"""
Module: database.mongodb.__init__

The `__init__.py` module initializes the MongoDB client and provides access to the database collection based on the environment.

Variables:
    - collection: MongoDB collection object representing the collection to interact with.

Usage:
    from database.mongodb import collection

    # Access the MongoDB collection
    chat_collection = collection
"""
import os
import dotenv

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# Load environment variables from .env file
dotenv.load_dotenv()

# Initialize MongoDB client and set up connection based on environment
if os.getenv("ENV") == "prod":
    # Production environment
    username = os.getenv("MONGO_DB_USERNAME")
    password = os.getenv("MONGO_DB_PASSWORD")

    # MongoDB Atlas URI
    uri = f"mongodb+srv://{username}:{password}@cluster0.n4hegjm.mongodb.net/?retryWrites=true&w=majority"

    # Create a new client and connect to the server
    client = MongoClient(uri, server_api=ServerApi("1"))

    # Access the database and collection
    database = client["chat_history_database"]
    collection = database["ccl_collection"]
else:
    # Development or local environment
    # Connect to local MongoDB instance
    collection = MongoClient("localhost", 27017)["testdb"]["test_collection"]
