from meta_property import export_data
import json
def split_full_name(full_name):
    if not full_name:
        return None, None
    name_parts = full_name.strip().split()
    return name_parts[0], " ".join(name_parts[1:]) if len(name_parts) > 1 else None

def get_agency():
    agency_in = export_data["agency"]
    return {
        "agencyId": agency_in["agencyId"],
        "banner": agency_in["branding"]["banner"]["url"],
        "contactDetails": agency_in["contactDetails"]["general"]["phone"],
        "isArchived": agency_in["isArchived"],
        "logo": agency_in["branding"]["logo"]["url"],
        "logosmall": agency_in["branding"]["logoSmall"]["url"],
        "name": agency_in["name"],
        "profileUrl": agency_in["profileUrl"],
        "website": agency_in["website"],
    }

def get_agents():
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

def get_images():
    return [{"category": "kitchen", "star": False, "url": url} for url in export_data["pro_meta"]["images"]]

def get_property_for_sale():
    pro_meta = export_data["pro_meta"]
    agents_info = get_agents()
    return {
        "architecturalStyle": None,
        "area": {"totalArea": pro_meta["landArea"], "unit": "sqM"},
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
            "lat": export_data["displayableAddress"]["geolocation"]["latitude"],
            "lng": export_data["displayableAddress"]["geolocation"]["longitude"],
        },
        "description": export_data.get("description", ""),
        "expectedPrice": export_data["saleInfo"]["expectedPrice"],
        "features": {
            "appliances": ["None"], "basement": "None", "buildingAmenities": ["None"],
            "coolingTypes": ["None"], "displayAddress": "fullAddress", "floorCovering": ["None"],
            "floorNo": 1, "garage": 1, "heatingFuels": ["None"], "heatingTypes": ["None"],
            "indoorFeatures": ["None"], "outdoorAmenities": ["None"], "parking": ["Carport"],
            "roof": ["Other"], "rooms": ["None"], "view": ["None"]
        },
        "historySale": export_data.get("historySale", []),
        "images": get_images(),
        "listingOption": export_data["saleInfo"]["listingOption"],
        "postcode": pro_meta.get("postcode", ""),
        "pricing": {
            "authority": export_data["saleInfo"]["pricing"]["authority"],
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
        "status": export_data["saleInfo"]["status"],
        "street": pro_meta["address"],
        "structuralRemodelYear": "N/A",
        "suburb": pro_meta["suburb"],
        "title": export_data["headline"],
        "url": export_data["url"],
    }
    
def get_schools():
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

def convert_property():
    return {
        "agency": get_agency(),
        "agent": get_agents(),
        "images": get_images(),
        "propertyForSale": get_property_for_sale(),
        "school": get_schools(),
    }

def export_to_json(data, file):
    with open(file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
        
export_to_json(convert_property(),"step2.json")