import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from motor.motor_asyncio import AsyncIOMotorClient

url = ""

client = AsyncIOMotorClient(url) 
database = client["aihomesearch"]
collection = {
    "Agency" : database["Agency"],
    "Agent" : database["Agent"],
    "School" : database["School"],
    "Image": database["Image"],
    "PropertyForSale" : database["PropertyForSale"]
}

