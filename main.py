from upload_new_data import PropertyDatabaseManager
import asyncio
from meta_property.convert_property import convert_property
from meta_property.meta_property import get_html_from_link, get_properties_data_from_html, access_data
import time
import csv

async def main():
    manager = PropertyDatabaseManager()
    with open(".database/st_lucia.csv", mode="r", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)
        urls = [row[1] for row in reader]
        htmls = await get_html_from_link(urls)
        for url, html in zip(urls, htmls):
            data = await get_properties_data_from_html(html)
            data = await access_data(data)
            data = await convert_property(data)
            await manager.create_property_for_sale(data, url)

if __name__ == "__main__":
    print("Starting: Please wait ...")
    start = time.time()
    asyncio.run(main())
    print(f"Time taken: {time.time() - start} seconds.")