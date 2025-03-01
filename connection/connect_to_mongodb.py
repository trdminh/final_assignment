import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from motor.motor_asyncio import AsyncIOMotorClient

url = "mongodb+srv://daven:ZDhibXswJ1LIFZx6@cluster0.qxlcce8.mongodb.net/"

client = AsyncIOMotorClient(url) 
database = client["aihomesearch"]
collection = {
    "Agency" : database["Agency"],
    "Agent" : database["Agent"],
    "School" : database["School"],
    "Image": database["Image"],
    "ImageSold" : database["ImageSold"],
    "PropertyForSale" : database["PropertyForSale"],
    "HistoryForSale" : database["HistoryForSale"],
    "PropertySold" : database["PropertySold"]
}

async def get_document_id(query, collection):
    result = await collection.find_one(query)  
    return result["_id"] if result else False  

async def get_emb_image(id):
    result = await collection["Image"].find_one({"_id": id})
    return result

