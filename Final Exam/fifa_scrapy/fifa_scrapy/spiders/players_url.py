import scrapy

class SofifaSpider(scrapy.Spider):
	name='players_url'

	custom_settings = {
		'ITEM_PIPELINES': {
			'fifa_scrapy.pipelines.FifaScrapyPipeline_URL': 300,
		}
	}

	def __init__(self):
		self.pages = 0

	def start_requests(self):
		urls = [
		# 'https://sofifa.com/players?offset=0'
		'https://sofifa.com/players?r=200048&set=true'
		]

		for url in urls:
			yield scrapy.Request(url=url, callback=self.parse)

	def parse(self, response):
		print(self.pages)
		for player in response.css('.col-name'):
			player_link = player.xpath('a/@href').re(r'/player/\w+')
			if len(player_link)	> 0:
				yield {
					'player_url': player_link[0]
				}

		next_page = response.xpath('.//div[@class="pagination"]/a[@class="bp3-button pjax"]/@href').extract()
		print(next_page)
		if next_page:
			if len(next_page) == 1:
				next_href = next_page[0]
			else:
				next_href = next_page[1]
			next_page_url = 'https://sofifa.com' + next_href
			print(next_page_url)
			self.pages += 1
			request = scrapy.Request(url=next_page_url)
			yield request