from connection.connect_to_mongodb import  collection
from database.database import Agency, Agent, School, Image, PropertyForSale
from datetime import datetime
from bson import ObjectId
import asyncio
from meta_property.convert_property import convert_property
from zero_short.zeroshort import classification, enhanced_classification
file = "/input/step1.html"
data = convert_property(file)
classification_images = enhanced_classification(data["images"])
async def create_agnecy_data(data):
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


async def create_agent_data(data):
    result_id = []
    for agent in data:
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
    return result_id
async def create_school_data(data):
    result_id = []
    for school in data:
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
    return result_id

async def create_image_data(data):
    result_id = []
    new_image = []
    for image in data:
        image_data = Image(
            category=image["predicted_category"],
            createdAt=datetime.now(),
            emb=image["emb"],
            star=image["star"],
            updatedAt=datetime.now(),
            url=image["url"]
        )
        data_upload_image = image_data.to_dict()
        result = await collection["Image"].insert_one(data_upload_image)
        new_image.append({"category": image["predicted_category"],"star":image["star"], "url": image["url"]})
        result_id.append(result.inserted_id)
    return result_id, new_image

async def created_property_for_sale(data):
    try:
        # Create agency data
        agency_id = await create_agnecy_data(data["agency"])
        print(f"Agency created with ID: {agency_id}")
        
        # Create agent datass
        agent_ids = await create_agent_data(data["agent"])
        print(f"Agents created with IDs: {agent_ids}")
        
        # Create school data
        school_ids = await create_school_data(data["school"])
        print(f"Schools created with IDs: {school_ids}")
        
        # Create image data
        image_ids, new_image = await create_image_data(enhanced_classification(data["images"]))
        print(f"Images created with IDs: {image_ids}")
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
            expectedPrice="N/A",
            features=data["propertyForSale"]["features"],
            historysale=data["propertyForSale"]["historySale"],
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
            updatedAt=datetime.now(),
            location={
                "type":"Point",
                "coordinates":[data["propertyForSale"]["coordinates"]["lng"], data["propertyForSale"]["coordinates"]["lat"]]
            }
        )
        result = await collection["PropertyForSale"].insert_one(property_for_sale.to_dict())
        print(f"Created PropertyForSale with ID: {result.inserted_id}")
    except Exception as e:
        print(f"An error occurred: {e}")

# # Run the main function
if __name__ == "__main__":
    asyncio.run(created_property_for_sale(data))