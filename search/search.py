import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from bs4 import BeautifulSoup
from crawl4ai import AsyncWebCrawler
import re
import json
from collections import OrderedDict

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
async def get_page(url):
    page_urls = []
    total = await get_total_pages(url)  # Lấy tổng số trang
    for page_number in range(1, int(total) + 1):
        paginated_url = f"{url}?page={page_number}"  # Tạo URL mới mà không ghi đè url gốc
        page_urls.append(paginated_url)
    return page_urls
async def get_links(url):
    urls = await get_page(url)
    all_links = []
    async with AsyncWebCrawler() as crawler:
        results = await crawler.arun_many(urls)
    for result in results:
        links = result.links["internal"]
        property_pattern = re.compile(r"https://www\.domain\.com\.au/.+-\d{10}")
        property_links = [link['href'] for link in links if property_pattern.match(link['href'])]
        all_links.append(property_links)
    
    return all_links
        



