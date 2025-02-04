import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import csv
from bs4 import BeautifulSoup
from crawl4ai import AsyncWebCrawler, WebCrawler
import re
import json
from collections import OrderedDict

# SEARCH_KEY = "6cbe87d71e8df219ac1bc71a0f7f6ea4b6b9956d336cf420de13783109dc3c37"

async def get_total_pages(url):
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url=url)

    # Phân tích HTML với BeautifulSoup
    soup = BeautifulSoup(result.html, "html.parser")
    script_tags = soup.find_all("script")

    for script in script_tags:
        if "digitalData" in script.text:
            try:
                json_text = script.text.split("var digitalData = ")[1].split(";")[0]
                data = json.loads(json_text)
                return data["page"]["pageInfo"]["search"]["resultsPages"]
            except Exception:
                continue

    return None  # Trả về None nếu không tìm thấy giá trị



# async def google_search_serpapi(session, query, num_results=10, filter=None):
#     """Search Google using SerpAPI """
#     url = "https://serpapi.com/search"
#     params = {
#         "q": query,
#         "hl": "en",
#         "gl": "au",
#         "num": num_results,
#         "api_key": SEARCH_KEY
#     }

#     async with session.get(url, params=params) as response:
#         if response.status != 200:
#             print(f"❌ Error {response.status}: Can't get links")
#             return []

#         data = await response.json()
#         links = [result["link"] for result in data.get("organic_results", []) if "link" in result]

#         if filter:
#             links = [link for link in links if filter in link]

#         return links


# async def property_search(query,filter="domain.com.au"):

#     async with aiohttp.ClientSession() as session:
#         results = await google_search_serpapi(session, query, num_results=20, filter=filter)

#     return results  # Return list of links



async def search_url(url):
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url=url)
    page_source = result.html
    soup = BeautifulSoup(page_source, "html.parser")
    search_results = soup.find_all("div")
    links = []
    for result in search_results:
        try:
            link = result.a["href"]
            if 'https://www.domain.com.au' in link:
                links.append(link)
        except:
            continue
    links = list(OrderedDict.fromkeys(links))
    return links
async def get_page_url(urls):
    urls = await search_url(url)
    for url in urls:
        if 'sale' in url  and 'house' not in url:
            sale_url = url
    return sale_url
async def filter_sale_urls(urls):
    excluded_urls = ['group', 'owners', 'property-profile', 'suburb-profile']
    prosale_urls = []
    
    for url in urls:
        if len(url) > len('https://www.domain.com.au/'):  # Bỏ qua trang chủ
            if 'sale' in url:  # Chỉ lấy URL có chứa "sale"
                if not any(excluded in url for excluded in excluded_urls):  # Không chứa các từ khóa bị loại trừ
                    prosale_urls.append(url)
    
    return prosale_urls

async def scraping_by_street(search_keyword):
    search_url_sale = "https://www.google.com/search?q=" + search_keyword
    urls = await search_url(search_url_sale) # get all domain links
    url = await filter_sale_urls(urls) # get for all property for sale links
    return url

async def get_links(url):
    all_links = []
    total_pages = await get_total_pages(url)
    pages = []
    for page_number in range(1, total_pages+1):
        pages.append(f"{url}?page={page_number}")
    for page_number in range(1, total_pages+1):
        async with AsyncWebCrawler() as crawler:
            result = await crawler.arun(url=f"{url}?page={page_number}")
        links = result.links['internal']
        property_pattern = re.compile(r"https://www\.domain\.com\.au/.+-\d{10}")
        property_links = [link['href'] for link in links if property_pattern.match(link['href'])]
        all_links.append(property_links)
        
    return all_links

async def main():
    results = await scraping_by_street("property for sale in sydney domain")
    all_links = await get_links(results[0])

    with open("url_database.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Page", "URL"])  

        for page_idx, links in enumerate(all_links, start=1):
            for link in links:
                writer.writerow([f"{page_idx}", link])  

    print("Ghi file CSV thành công!")
    


import asyncio  
asyncio.run(main())