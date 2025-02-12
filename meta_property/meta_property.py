import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import re
import json

file_path = 'input/step1'


def get_properties_data_from_html(file):
    with open(file_path, 'r', encoding='utf-8') as file:
        file_content = file.read()


    script_pattern = r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>'
    match = re.search(script_pattern, file_content, re.DOTALL)

    if match:
        next_data_content = match.group(1)
        try:
            next_data_json = json.loads(next_data_content)
        except json.JSONDecodeError as e:
            next_data_json = f"Error decode JSON: {e}"
    else:
        next_data_json = "Can't find <script> with id='__NEXT_DATA__'."
    return next_data_json

def find_key(data, key_to_find):
    if isinstance(data, dict):
        for key, value in data.items():
            if key == key_to_find:
                return value
            result = find_key(value, key_to_find)
            if result is not None:
                return result
    elif isinstance(data, list):
        for item in data:
            result = find_key(item, key_to_find)
            if result is not None:
                return result
    return None


def get_history_sale(file):
    data_json = get_properties_data_from_html(file)
    root_graph_query = find_key(data_json, "rootGraphQuery")
    historySale = {}
    historySale["agencyId"] = root_graph_query["listingByIdV2"]["agency"]
    if find_key(data_json, "soldDate") == None:
        historySale["soldDate"] = None
    if find_key(data_json, "soldPrice") == None:
        historySale["soldPrice"] = None
    
    return historySale


def get_sale_info(file):
    data_json = get_properties_data_from_html(file)
    saleInfo = {}
    if find_key(data_json, "expectedPrice") == None:
        saleInfo["expectedPrice"] = None
    else:
        saleInfo["expectedPrice"] = find_key(data_json, "expectedPrice")
    saleInfo["listingOption"] = find_key(data_json, "onMarketType")
    pricing = {}
    if saleInfo["listingOption"] == "sale":
        pricing["authority"] = "for-sale"
    else:
        pricing["authority"] = "not-for-sale"
    if find_key(data_json, "priceIncludes") == None:
        pricing["priceIncludes"] = ['']
    else:
        pricing["priceIncludes"] = find_key(data_json, "priceIncludes")
    pricing["pricingOptions"] = find_key(data_json, "price")
    saleInfo["pricing"] = pricing
    if find_key(data_json, "soldDateInfo") == None:
        saleInfo["soldDateInfo"] = None
    else:
        saleInfo["soldDateInfo"] = find_key(data_json, "soldDateInfo")
    saleInfo["status"] = saleInfo["pricing"]["authority"]
    
    return saleInfo

def access_data(file):
    data_json = get_properties_data_from_html(file)
    root_graph_query = find_key(data_json, "rootGraphQuery")
    school_catchment = find_key(data_json, "schoolCatchment")
    prometa = find_key(data_json, "page")
    return {
    "agency" : root_graph_query["listingByIdV2"]["agency"],
    "agentProfiles" : root_graph_query["listingByIdV2"]["agents"],
    "description" : root_graph_query["listingByIdV2"]["description"],
    "displayableAddress" : root_graph_query["listingByIdV2"]["displayableAddress"],
    "headline" : root_graph_query["listingByIdV2"]["headline"],
    "historySale" : get_history_sale(file),
    "pro_meta" : prometa["pageInfo"]["property"],
    "propertyType" : {"propertyType":find_key(data_json, "propertyType")},
    "school" : school_catchment["schools"],
    "saleInfo" : get_sale_info(file),
    "slug" : {"slug": find_key(data_json, "propertyProfileUrlSlug")},
    "structuredFeatures" : find_key(data_json, "structuredFeatures"),
    "totalarea" : find_key(data_json, "landArea"),
    "url" : find_key(data_json, "canonical")
    }
