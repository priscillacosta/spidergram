import scrapy
import json

class Spidergram(scrapy.Spider):
    name = "Insta"

    def __init__(self):
        self.account = input("Name of the account? ")
        self.start_urls = ["https://www.instagram.com/" + self.account]

    def parse(self, response):
        request = scrapy.Request(response.url, callback=self.parse_page)
        return request

    def parse_page(self, response):
        js = response.selector.xpath('//script[contains(., "window._sharedData")]/text()').extract()
        js = js[0].replace("window._sharedData = ", "")
        jscleaned = js[:-1]

        data = json.loads(jscleaned)
        user = data['entry_data']['ProfilePage'][0]['user']
        has_next = user['media']['page_info']['has_next_page']
        media = user['media']['nodes']

        for photo in media:
            url = photo['display_src']
            id = photo['id']
            is_video = photo['is_video']

            if is_video:
                continue

            yield scrapy.Request(url, 
                meta={'id' : id, 'extension' : '.jpg'},
                callback=self.save_media)

        if has_next:
            url="https://www.instagram.com/" + self.account + "/?max_id=" + media[-1]['id']
            yield scrapy.Request(url, callback=self.parse_page)