import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from meta_property.meta_property import find_key

import re
def split_full_name(full_name):
    if not full_name:
        return None, None
    name_parts = full_name.strip().split()
    return name_parts[0], " ".join(name_parts[1:]) if len(name_parts) > 1 else None

async def get_agency(export_data):
    agency_in = export_data["agency"]
    return {
        "agencyId": agency_in["agencyId"],
        "banner": find_key(agency_in["branding"]["banner"], "url"),
        "contactDetails": agency_in["contactDetails"]["general"]["phone"],
        "isArchived": agency_in["isArchived"],
        "logo": find_key(agency_in["branding"]["logo"],"url"),
        "logosmall": find_key(agency_in["branding"]["logoSmall"],"url"),
        "name": agency_in["name"],
        "profileUrl": agency_in["profileUrl"],
        "website": agency_in["website"],
    }
async def get_features(export_data):
    indoorFeatures = []
    outdoorAmenities = []
    if export_data["features"] is None:
        indoorFeatures = ["None"]
        outdoorAmenities = ["None"]
        return indoorFeatures, outdoorAmenities
    else:
        for feature in export_data["features"]:
            if "category" in feature and  feature["category"] == "Indoor":
                indoorFeatures.append(feature["name"])
            elif "category" in feature and feature["category"] == "Outdoor":
                outdoorAmenities.append(feature["name"])
        return indoorFeatures, outdoorAmenities
    
        
async def get_agents(export_data):
    agents_in = export_data["agentProfiles"]
    return [
        {
            "agentId": agent["agentId"],
            "email": agent["email"],
            "firstName": split_full_name(agent["fullName"])[0],
            "lastName": split_full_name(agent["fullName"])[1],
            "isActiveProfilePage": agent["isActiveProfilePage"],
            "phoneNumber": agent["mobileNumber"],
            "photo": agent["photo"]["url"],
            "profileUrl": agent["profileUrl"],
        }
        for agent in agents_in
    ]

async def get_images(export_data):
    return [{"category": "kitchen", "star": False, "url": url} for url in export_data["pro_meta"]["images"]]



async def get_excepted_price(text):
    price_pattern = re.compile(r'\$([\d,.]+[kKmM]?)')
    match = price_pattern.findall(text)
    status = "sold" if "SOLD" in text.upper() else "for-sale"
    
    if not match:
        return {"price": "N/A", "status": status}
    
    prices = []
    for price in match:
        numeric_price = price.replace('.', '').replace(',', '')
        if 'k' in numeric_price.lower():
            numeric_price = float(numeric_price[:-1]) * 1000
        elif 'm' in numeric_price.lower():
            numeric_price = float(numeric_price[:-1]) * 1000000
        else:
            numeric_price = float(numeric_price)
        prices.append(numeric_price)
    
    if len(prices) > 1:
        avg_price = sum(prices) / len(prices)
        return {"price": f"${avg_price:,.0f}", "status": status}
    
    return {"price": f"${prices[0]:,.0f}", "status": status}

async def format_money(value: str) -> str:
    if value[-1].upper() == 'K':  
        try:
            number = float(value[:-1]) * 1000
            return f"${number:,.0f}"
        except ValueError:
            return "N/A"
    elif value[-1].upper() == 'M':
        try:
            number = float(value[:-1]) * 1000000
            return f"${number:,.0f}"
        except ValueError:
            return "N/A"
    elif value[-1].upper() == 'B':
        try:
            number = float(value[:-1]) * 1000000000
            return f"${number:,.0f}"
        except ValueError:
            return "N/A"
    return "N/A"

async def get_history_sale(export_data):
    agents_info = await get_agents(export_data)
    price_options = await get_excepted_price(export_data["historySale"]["soldPrice"])
    indoorFeatures, outdoorAmenities = await get_features(export_data)
    return {
        "historyprofile": [{
            "stakeHolder": "agent",
            "soldDateInfo": export_data["historySale"]["soldDateInfo"],
           "contractInfo": [
            {
                "email": agent["email"],
                "firstName": agent["firstName"],
                "lastName": agent["lastName"],
                "startDate": None,
                "status": "current",
            }
                for agent in agents_info
            ],
           "title": export_data["headline"],
           "slug": export_data["slug"]["slug"],
            "propertyType": export_data["propertyType"]["propertyType"],
            "description": export_data["description"],
            "bed": export_data["pro_meta"]["bedrooms"],
            "bath": export_data["pro_meta"]["bathrooms"],
            "images": await get_images(export_data),
            "features": {
                "garage": 6,
                "floorno": 1,
                "basement": "None",
                "floorCovering": ["None"],
                "parking": ["Carport"],
                "roof": ["Other"],
                "view": ["None"],
                "rooms": ["None"],
                "indoorFeatures": indoorFeatures,
                "coolingTypes": ["None"],
                "heatingTypes": ["None"],
                "heatingFuels": ["None"],
                "appliances": ["None"],
                "buildingAmenities": ["None"],
                "outdoorAmenities": outdoorAmenities,
                "displayAddress": "fullAddress"
            },
            "area": {"totalArea": export_data["totalarea"], "unit": "sqM"},
            "historySale": [{
                "soldDate": {export_data["historySale"]["soldDate"],
                },
                "agencyId": export_data["agency"]["agencyId"],
                "soldPrice": "N/A" if price_options["price"] == "$0" else price_options["price"],
                "dayslisted": None,
            }]
        } 
        ],
    }
async def get_property_for_sale(export_data):
    pro_meta = export_data["pro_meta"]
    agents_info = await get_agents(export_data)
    price_options = await get_excepted_price(export_data["saleInfo"]["pricing"]["pricingOptions"])
    soldprice = await format_money(export_data["historySale"]["soldPrice"])
    indoorFeatures, outdoorAmenities = await get_features(export_data)
    return {
        "architecturalStyle": None,
        "area": {"totalArea": export_data["totalarea"], "unit": "sqM"},
        "bath": pro_meta["bathrooms"],
        "bed": pro_meta["bedrooms"],
        "city": "Unincorporated Act",
        "constructionYear": "N/A",
        "contractInfo": [
            {
                "email": agent["email"],
                "firstName": agent["firstName"],
                "lastName": agent["lastName"],
                "startDate": None,
                "status": "current",
            }
            for agent in agents_info
        ],
        "coordinates": {
            "lat": find_key(export_data["displayableAddress"],"latitude"),
            "lng": find_key(export_data["displayableAddress"],"longitude"),
        },
        "description": export_data.get("description", ""),
        "expectedPrice": "N/A" if price_options["price"] == "$0"  else price_options["price"],
        "features": {
            "appliances": ["None"], "basement": "None", "buildingAmenities": ["None"],
            "coolingTypes": ["None"], "displayAddress": "fullAddress", "floorCovering": ["None"],
            "floorNo": 1, "garage": 1, "heatingFuels": ["None"], "heatingTypes": ["None"],
            "indoorFeatures": indoorFeatures, "outdoorAmenities": outdoorAmenities, "parking": ["Carport"],
            "roof": ["Other"], "rooms": ["None"], "view": ["None"]
        },
        "historySale": {
                "soldDate": None,
                "agencyId": export_data["historySale"]["agencyId"],
                "soldPrice": soldprice,
                "dayslisted": export_data["historySale"]["soldDate"],
            },
        "images": await get_images(export_data),
        "listingOption": export_data["saleInfo"]["listingOption"],
        "postcode": pro_meta.get("postcode", ""),
        "pricing": {
            "authority": price_options["status"],
            "councilBill": "",
            "priceIncludes": export_data["saleInfo"]["pricing"]["priceIncludes"],
            "pricingOptions": export_data["saleInfo"]["pricing"]["pricingOptions"],
            "waterBillPeriod": "monthly",
        },
        "propertyType": pro_meta["primaryPropertyType"],
        "published": False,
        "recommended": False,
        "slug": export_data["slug"]["slug"],
        "stakeHolder": "agent",
        "state": pro_meta["state"],
        "status": price_options["status"],
        "street": pro_meta["address"],
        "structuralRemodelYear": "N/A",
        "suburb": pro_meta["suburb"],
        "title": export_data["headline"],
        "url": export_data["url"],
    }
    
async def get_schools(export_data):
    return [
        {
            "address":school["address"],
            "distances":school["distance"],
            "domainSeoUrlSlug":school["domainSeoUrlSlug"],
            "educationLevel":school["educationLevel"],
            "gender":school["gender"],
            "name":school["name"],
            "postcode":school["postCode"],
            "state":school["state"],
            "status":school["status"],
            "type":school["type"],
            "url":school["url"],
            "year":school["year"],
        }
    for school in export_data["school"]
    ]

async def convert_property(export_data):
    return {
        "agency": await get_agency(export_data),
        "agent": await get_agents(export_data),
        "images": await get_images(export_data),
        "propertyForSale": await get_property_for_sale(export_data),
        "school": await get_schools(export_data),
    }

