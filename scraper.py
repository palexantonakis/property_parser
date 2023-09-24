import scrapy
import json
import pandas as pd
from scrapy.crawler import CrawlerProcess

class propertySpider(scrapy.Spider):
    name = 'property_spider'
    start_urls  = ['https://www.sreality.cz/api/en/v2/estates?category_main_cb=1&category_type_cb=1&per_page=500']

    def parse(self, response):
        # Parse the JSON response
        data = json.loads(response.text)        
        global df
        df = pd.json_normalize(data['_embedded']['estates'])

# Create a CrawlerProcess
process = CrawlerProcess()

# Add your spider to the process
process.crawl(propertySpider)

# Start the process
process.start()

# data processing
to_write = df[['name', '_links.image_middle2']].rename(columns={'_links.image_middle2': 'photo'})
to_write.index = to_write.index + 1
to_write = to_write.reset_index()
to_write['photo'] = [x[0]['href'] for x in to_write['photo']]