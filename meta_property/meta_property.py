import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import re
import json
from search.search import get_links, scraping_by_street
from crawl4ai import AsyncWebCrawler



async def get_html_from_link(all_link):
    async with AsyncWebCrawler() as crawler:
        property_sales = await crawler.arun_many(all_link)
    result = []
    for property_sale in property_sales:
        result.append(property_sale.html)
    return result

async def get_properties_data_from_html(file_html):
    script_pattern = r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>'
    match = re.search(script_pattern, file_html, re.DOTALL)

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


async def get_history_sale(data_json):
    root_graph_query = find_key(data_json, "rootGraphQuery")
    historySale = {}
    historySale["agencyId"] = root_graph_query["listingByIdV2"]["agency"]
    historySale["soldDate"] = find_key(data_json, "dateListed")
    historySale["soldPrice"] = find_key(data_json,"medianPrice")
    
    return historySale


async def get_sale_info(data_json):
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
        pricing["authority"] = "sold"
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

async def access_data(data_json):
    root_graph_query = find_key(data_json, "rootGraphQuery")
    school_catchment = find_key(data_json, "schoolCatchment")
    prometa = find_key(data_json, "page")
    return {
    "agency" : find_key(root_graph_query,"agency"),
    "agentProfiles" : find_key(root_graph_query["listingByIdV2"],"agents"),
    "description" : find_key(root_graph_query["listingByIdV2"],"description"),
    "displayableAddress" : find_key(root_graph_query["listingByIdV2"],"displayableAddress"),
    "headline" : find_key(root_graph_query["listingByIdV2"],"headline"),
    "historySale" : await get_history_sale(data_json),
    "pro_meta" : prometa["pageInfo"]["property"],
    "price": find_key(data_json, "price"),
    "propertyType" : {"propertyType":find_key(data_json, "propertyType")},
    "school" : school_catchment["schools"],
    "saleInfo" : await get_sale_info(data_json),
    "slug" : {"slug": find_key(data_json, "propertyProfileUrlSlug")},
    "structuredFeatures" : find_key(data_json, "structuredFeatures"),
    "totalarea" : find_key(data_json, "landArea"),
    "url" : find_key(data_json, "canonical"),
    "features" : find_key(data_json, "structuredFeatures"),
    }

