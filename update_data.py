from connection.connect_to_mongodb import collection,database
from tornado.ioloop import IOLoop
# async def f():
#     count = await collection["PropertyForSale"].count_documents({})
#     print("Final count: %d" % count)

from pprint import pprint
from pymongo import InsertOne, DeleteMany, ReplaceOne, UpdateOne
from zero_short.zeroshort import enhanced_classification
async def f():
    result = await database.test.bulk_write(
        [
            DeleteMany({}),  # Remove all documents from the previous example.
            InsertOne({"_id": 1}),
            InsertOne({"_id": 2}),
            InsertOne({"_id": 3}),
            UpdateOne({"_id": 1}, {"$set": {"foo": "bar"}}),
            UpdateOne({"_id": 4}, {"$inc": {"j": 1}}, upsert=True),
            ReplaceOne({"j": 1}, {"j": 2}),
        ]
    )
    pprint(result.bulk_api_result)


async def get_embedding_from_db(image_url):
    """Truy xuất embedding từ collection Image bằng URL"""
    image_doc = await collection["ImageSold"].find_one({"url": image_url}, {"emb": 1})  # Chỉ lấy trường emb
    return image_doc["emb"] if image_doc and "emb" in image_doc else None

async def update_missing_embeddings():
    """Tìm và cập nhật embeddings bị thiếu từ collection Image"""
    cursor = collection["PropertySold"].find({"images.emb": None})

    async for doc in cursor:
        updated_images = []
        for image in doc.get("images", []):
            if "emb" not in image or image["emb"] is None:
                image_url = image.get("url")
                if image_url:
                    embedding = await get_embedding_from_db(image_url)
                    if embedding:
                       
                        image_list = list(image.items())  
                        image_list.insert(1, ("emb", embedding))  
                        image = dict(image_list)  
            updated_images.append(image)


        await collection["PropertySold"].update_one(
            {"_id": doc["_id"]},
            {"$set": {"images": updated_images}}
        )
        print(f"Updated document {doc['_id']}")



IOLoop.current().run_sync(lambda: update_missing_embeddings())
