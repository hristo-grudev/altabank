import json

import scrapy

from scrapy.loader import ItemLoader
from w3lib.html import remove_tags

from ..items import AltabankItem
from itemloaders.processors import TakeFirst

base = 'https://altabank.com/wp-json/wp/v2/posts/?_fields=id,slug,title,featured_media,link,categories,excerpt,better_featured_image,date,modified,content&per_page=100&page={}'


class AltabankSpider(scrapy.Spider):
	name = 'altabank'
	page = 1
	start_urls = [base.format(page)]

	def parse(self, response):
		data = json.loads(response.text)
		for post in data:
			title = post['title']['rendered']
			date = post['date']
			description = remove_tags(post['content']['rendered'])

			item = ItemLoader(item=AltabankItem(), response=response)
			item.default_output_processor = TakeFirst()
			item.add_value('title', title)
			item.add_value('description', description)
			item.add_value('date', date)

			yield item.load_item()

		if len(data) == 100:
			self.page += 1
			yield response.follow(base.format(self.page), self.parse)



