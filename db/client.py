## MongoDB client ###
import asyncio
import os
from dotenv import load_dotenv
from typing import Optional, List



load_dotenv()

from pymongo import ReturnDocument
from motor.motor_asyncio import AsyncIOMotorClient

client: AsyncIOMotorClient = AsyncIOMotorClient(os.environ.get("DATA_BASE_URL_ATLAS"))
#? client.get_io_loop = asyncio.get_running_loop

db = client.eventhor
users_collection = db.get_collection("User")
topics_collection = db.get_collection("Topic")
questions_collection = db.get_collection("Question")