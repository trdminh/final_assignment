from connection.connect_to_mongodb import  collection, get_document_id
from database.database import Agency, Agent, School, Image, PropertyForSale, HistoryForSale, PropertySold
from datetime import datetime
from bson import ObjectId

import asyncio
from meta_property.convert_property import convert_property
from meta_property.meta_property import get_html_from_link, get_properties_data_from_html, access_data
from zero_short.zeroshort import enhanced_classification
from zero_short.nomic_emb_v1 import emb_semantic_nomic

async def create_agency_data(data):
    
    if await get_document_id({"profileUrl": data["profileUrl"]}, collection["Agency"]) == False:
        agency = Agency(
            agencyId=data["agencyId"],
            banner=data["banner"],
            contactDetails=data["contactDetails"],
            createdAt=datetime.now(),
            logo=data["logo"],
            logoSmall=data["logosmall"],
            name=data["name"],
            profileUrl=data["profileUrl"],
            updatedAt=datetime.now(),
            website=data["website"]
        )
        
        data_dict = agency.to_dict()
        # Upload to MongoDB 
        result = await collection["Agency"].insert_one(data_dict)
        return result.inserted_id
    else:
        return await get_document_id({"website": data["website"]}, collection["Agency"])


async def create_agent_data(data):
    result_id = []
    for agent in data:
        
        if await get_document_id({"email": agent["email"]}, collection["Agent"]) == False:
            agent_data = Agent(
                agentId=agent["agentId"],
                createdAt=datetime.now(),
                email=agent["email"],
                firstName=agent["firstName"],
                isActiveProfilePage=agent["isActiveProfilePage"],
                lastName=agent["lastName"],
                phoneNumber=agent["phoneNumber"],
                photo=str(agent["photo"]),
                profileUrl=agent["profileUrl"],
                updatedAt=datetime.now()
            )
            
            data_upload_agent = agent_data.to_dict()
            #Upload
            result = await collection["Agent"].insert_one(data_upload_agent)
            result_id.append(result.inserted_id)
        else: 
            result_id.append(await get_document_id({"email": agent["email"]}, collection["Agent"]))
    return result_id
async def create_school_data(data):
    result_id = []
    for school in data:
        
        if await get_document_id({"url":school["url"]}, collection["School"]) == False:
            school_data = School(
                address=school["address"],
                createdAt=datetime.now(),
                distance=school["distances"],
                domainSeoUrlSlug=school["domainSeoUrlSlug"],
                educationLevel=school["educationLevel"],
                gender=school["gender"],
                name=school["name"],
                postCode=school["postcode"],
                state=school["state"],
                type=school["type"],
                updatedAt=datetime.now(),
                url=school["url"],
                year=school["year"]
            )
            
            data_upload_school = school_data.to_dict()
            #Upload
            result = await collection["School"].insert_one(data_upload_school)
            result_id.append(result.inserted_id)
        else:
            result_id.append(await get_document_id({"url":school["url"]}, collection["School"]))
    return result_id

async def create_image_data(data, status,image_flag=True):
    result_id = []
    new_image = []

    for image in data:
        existing_id = await get_document_id({"url": image["url"]}, collection["Image"]) if status == "for-sale" else await get_document_id({"url": image["url"]}, collection["ImageSold"])

        if not existing_id:
            image_data = Image(
                category=image["category"],
                createdAt=datetime.now(),
                emb=image["emb"] if image_flag==True else None,
                star=image["star"],
                updatedAt=datetime.now(),
                url=image["url"]
            )
            data_upload_image = image_data.to_dict()
            result = await collection["Image"].insert_one(data_upload_image) if status == "for-sale" else await collection["ImageSold"].insert_one(data_upload_image)
            inserted_id = result.inserted_id
        else:
            inserted_id = existing_id

        result_id.append(inserted_id)
        new_image.append({
            "category": image["category"],
            "emb": image["emb"],
            "star": image["star"],
            "url": image["url"]
        })

    return result_id, new_image

async def created_history_for_sale(data,url,img_id,img,agencyid,agentid):
    historyforsale = HistoryForSale(
        createdAt=datetime.now(),
        historyprofile=[
            {
            "stackholder":data["propertyForSale"]["stakeHolder"],
            "soldDateInfo":data["propertyForSale"]["historySale"]["soldDate"],
            "contractInfo":data["propertyForSale"]["contractInfo"],
            "title":data["propertyForSale"]["title"],
            "slug":data["propertyForSale"]["slug"],
            "propertyType":data["propertyForSale"]["propertyType"],
            "description":data["propertyForSale"]["description"],
            "bed":data["propertyForSale"]["bed"],
            "bath":data["propertyForSale"]["bath"],
            "images":img,
            "features":data["propertyForSale"]["features"],
            "area":data["propertyForSale"]["area"],
            "historysale":[data["propertyForSale"]["historySale"]],
            "agencyid":agencyid,
            "agentid":agentid,
            "imageid":img_id,
        }
        ],
        updatedAt=datetime.now(),
        url=url
    )
    
    if await get_document_id({"url": url}, collection["HistoryForSale"]) == False:
        data_upload_history = historyforsale.to_dict()
        result = await collection["HistoryForSale"].insert_one(data_upload_history)
        return result.inserted_id
    else:
        return await get_document_id({"url": url}, collection["HistoryForSale"])
        
           

async def created_property_for_sale(data,url):
    try:
        
            # print(f"HistoryForSale created with ID: {history_id}")
        if data["propertyForSale"]["status"] == "for-sale":
            
            if await get_document_id({"url": url}, collection["PropertyForSale"]) == False:
                # Create agency data
                agency_id = await create_agency_data(data["agency"])
            # print(f"Agency created with ID: {agency_id}")
        
            # Create agent datass
                agent_ids = await create_agent_data(data["agent"])
            # print(f"Agents created with IDs: {agent_ids}")
        
            # Create school data
                school_ids = await create_school_data(data["school"])
            # print(f"Schools created with IDs: {school_ids}")
        
            # Create image data
                image_ids, new_image = await create_image_data(await enhanced_classification(data["images"]),image_flag=True,status=data["propertyForSale"]["status"])
        # print(f"Images created with IDs: {image_ids}")
        
                history_id = await created_history_for_sale(data,url,image_ids,new_image,agency_id,agent_ids)
                property_for_sale = PropertyForSale(
                    agencyId=ObjectId(agency_id),
                    agentId=agent_ids,
                    architecturalStyte=False,
                    area=data["propertyForSale"]["area"],
                    bath=data["propertyForSale"]["bath"],
                    bed=data["propertyForSale"]["bed"],
                    city=data["propertyForSale"]["city"],
                    constructionYear=data["propertyForSale"]["constructionYear"],
                    contactInfo=data["propertyForSale"]["contractInfo"],
                    coordinates=data["propertyForSale"]["coordinates"],
                    createdAt=datetime.now(),
                    description=data["propertyForSale"]["description"],
                    expectedPrice=data["propertyForSale"]["expectedPrice"],
                    features=data["propertyForSale"]["features"],
                    historysale=[{
                        "historyId": history_id,
                        "soldDate": None,
                        "agencyId": data["agency"].get("agencyId"),
                        "soldPrice": None,
                        "daylisted": None
                    }],
                    imageid=image_ids,
                    images=new_image,
                    listingOption=data["propertyForSale"]["listingOption"],
                    postcode=data["propertyForSale"]["postcode"],
                    pricing=data["propertyForSale"]["pricing"],
                    propertyType=data["propertyForSale"]["propertyType"],
                    published=data["propertyForSale"]["published"],
                    recommended=data["propertyForSale"]["recommended"],
                    schoolId=school_ids,
                    slug=data["propertyForSale"]["slug"],
                    stakeholder=data["propertyForSale"]["stakeHolder"],
                    state=data["propertyForSale"]["state"],
                    status=data["propertyForSale"]["status"],
                    street=data["propertyForSale"]["street"],
                    structuralRemodelYear=data["propertyForSale"]["structuralRemodelYear"],
                    suburb=data["propertyForSale"]["suburb"],
                    title=data["propertyForSale"]["title"],
                    embSemanticNomicTextV1=await emb_semantic_nomic(data["propertyForSale"],proid=True, pro_col=True),
                    updatedAt=datetime.now(),
                    url=url,
                    location={
                        "type":"Point",
                        "coordinates":[data["propertyForSale"]["coordinates"]["lng"], data["propertyForSale"]["coordinates"]["lat"]]
                    }
                )
                result = await collection["PropertyForSale"].insert_one(property_for_sale.to_dict())
                print(f"Created PropertyForSale with ID: {result.inserted_id}")
            else:
                except_id = await get_document_id({"url": url}, collection["PropertyForSale"])
                # await collection["PropertyForSale"].update_one(
                #     {"_id": ObjectId(except_id)},
                #     {"$set": property_for_sale}
                # )
                print(f"Updated PropertyForSale with ID: {except_id}")
        else:
            if await get_document_id({"url": url}, collection["PropertySold"]) == False:

                agency_id = await create_agency_data(data["agency"])

                agent_ids = await create_agent_data(data["agent"])

                school_ids = await create_school_data(data["school"])

        

                image_ids, new_image = await create_image_data(await enhanced_classification(data["images"]),image_flag=True,status=data["propertyForSale"]["status"])

                history_id = await created_history_for_sale(data,url,image_ids,new_image,agency_id,agent_ids)
                property_sold = PropertySold(
                agencyId=ObjectId(agency_id),
                agentId=agent_ids,
                architecturalStyte=False,
                area=data["propertyForSale"]["area"],
                bath=data["propertyForSale"]["bath"],
                bed=data["propertyForSale"]["bed"],
                city=data["propertyForSale"]["city"],
                constructionYear=data["propertyForSale"]["constructionYear"],
                contactInfo=data["propertyForSale"]["contractInfo"],
                coordinates=data["propertyForSale"]["coordinates"],
                createdAt=datetime.now(),
                description=data["propertyForSale"]["description"],
                expectedPrice=data["propertyForSale"]["expectedPrice"],
                features=data["propertyForSale"]["features"],
                historysale=[{
                    "historyId": history_id,
                    "soldDate": data["propertyForSale"]["historySale"]["soldDate"],
                    "agencyId": data["agency"]["agencyId"],
                    "soldPrice": data["propertyForSale"]["historySale"]["soldPrice"],
                    "daylisted": None
                }],
                imageid=image_ids,
                images=new_image,
                listingOption=data["propertyForSale"]["listingOption"],
                postcode=data["propertyForSale"]["postcode"],
                pricing=data["propertyForSale"]["pricing"],
                propertyType=data["propertyForSale"]["propertyType"],
                published=data["propertyForSale"]["published"],
                recommended=data["propertyForSale"]["recommended"],
                schoolId=school_ids,
                slug=data["propertyForSale"]["slug"],
                stakeholder=data["propertyForSale"]["stakeHolder"],
                state=data["propertyForSale"]["state"],
                status=data["propertyForSale"]["status"],
                street=data["propertyForSale"]["street"],
                structuralRemodelYear=data["propertyForSale"]["structuralRemodelYear"],
                suburb=data["propertyForSale"]["suburb"],
                title=data["propertyForSale"]["title"],
                embSemanticNomicTextV1=await emb_semantic_nomic(data["propertyForSale"],proid=True, pro_col=True),
                updatedAt=datetime.now(),
                url=url,
                location={
                    "type":"Point",
                    "coordinates":[data["propertyForSale"]["coordinates"]["lng"], data["propertyForSale"]["coordinates"]["lat"]]
                }
            )
                result = await collection["PropertySold"].insert_one(property_sold.to_dict())
                print(f"Created PropertySold with ID: {result.inserted_id}")
            else:
                except_id = await get_document_id({"url": url}, collection["PropertySold"])
                # await collection["PropertySold"].update_one(
                #     {"_id": ObjectId(except_id)},
                #     {"$set": property_for_sale}
                # )
                print(f"Updated PropertySold with ID: {except_id}")
    except Exception as e:
        print(e)
        with open("error.csv","a") as f:
            f.write(f"{str(e)}\n")
import time
import csv
async def main():
    with open(".database/st_lucia.csv", mode="r", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)
        urls = [row[1] for row in reader]
        htmls = await get_html_from_link(urls)
        for url, html in zip(urls, htmls):
            data = await get_properties_data_from_html(html)
            data = await access_data(data)
            data = await convert_property(data)
            await created_property_for_sale(data,url)
            # print(data)
if __name__ == "__main__":     
    print("Starting: Please wait ...")
    start = time.time()
    asyncio.run(main())
    print(f"Time taken: {time.time() - start} seconds.") 