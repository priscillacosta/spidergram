import scrapy
import json
import os
import urllib

class Spidergram(scrapy.Spider):
    name = "Spidergram"

    def __init__(self, account='', *args, **kwargs):
        super(Spidergram, self).__init__(*args, **kwargs)
        self.account = account
        self.start_urls = ["https://www.instagram.com/" + self.account]
        self._setup_folder()

    def _setup_folder(self):
        self.save_dir = 'users/' + self.account

        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)

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

    def save_media(self, response):
        response_id = response.meta['id']
        extension = response.meta['extension']
        fullfilename = os.path.join(self.save_dir, response_id + extension)
        urllib.request.urlretrieve(response.url, fullfilename)
