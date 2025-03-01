from search.search import scraping_by_street, get_links
import csv
import asyncio
import os
async def main():
    search_keyword = "property for sale in st lucia domain"
    url = await scraping_by_street(search_keyword) 
    if not url: 
        print("Không tìm thấy URL nào.")
        return
    print(url)
    
    all_link = await get_links(url[0])
    database_dir = os.path.join(os.getcwd(), ".database")
    os.makedirs(database_dir, exist_ok=True) 

    file_path = os.path.join(database_dir, "st_lucia.csv")

    with open(file_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["index", "url"])

        for index, link in enumerate(all_link, start=1):
            writer.writerow([index, link])

    print(f"save to: {file_path}")

asyncio.run(main())