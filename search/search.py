import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import aiohttp
from bs4 import BeautifulSoup
from crawl4ai import AsyncWebCrawler
import re
import json

SEARCH_KEY = "6cbe87d71e8df219ac1bc71a0f7f6ea4b6b9956d336cf420de13783109dc3c37"

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



async def google_search_serpapi(session, query, num_results=10, filter=None):
    """Search Google using SerpAPI """
    url = "https://serpapi.com/search"
    params = {
        "q": query,
        "hl": "en",
        "gl": "au",
        "num": num_results,
        "api_key": SEARCH_KEY
    }

    async with session.get(url, params=params) as response:
        if response.status != 200:
            print(f"❌ Error {response.status}: Can't get links")
            return []

        data = await response.json()
        links = [result["link"] for result in data.get("organic_results", []) if "link" in result]

        if filter:
            links = [link for link in links if filter in link]

        return links


async def property_search(query,filter="domain.com.au"):

    async with aiohttp.ClientSession() as session:
        results = await google_search_serpapi(session, query, num_results=20, filter=filter)

    return results  # Return list of links

async def get_links(url):
    all_links = []
    total_pages = await get_total_pages(url)
    for page_number in range(1, total_pages):
        async with AsyncWebCrawler() as crawler:
            result = await crawler.arun(url=f"{url}?page={page_number}")
        links = result.links['internal']
        property_pattern = re.compile(r"https://www\.domain\.com\.au/.+-\d{10}")
        property_links = [link['href'] for link in links if property_pattern.match(link['href'])]
        all_links.append(property_links)
        
    return all_links
