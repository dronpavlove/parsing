import requests
from bs4 import BeautifulSoup as Soup


class Client:

	def __init__(self):
		self.session = requests.Session()
		self.session.headers = {
			'Accept-Language': 'ru',
			'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36'
		}

	def load_page(self):
		url = 'https://www.wildberries.ru/catalog/novyy-god/elki'
		res = self.session.get(url=url)
		res.raise_for_status()
		return res.text

	def parse_page(self):
		a = []
		text = self.load_page()
		soup = Soup(text, 'lxml')
		container = soup.select('div.catalog-page__main.new-size') #  'div.product-card.j-card-item.j-good-for-listing-event')
		for block in container:
			a.append(self.parse_block(block=block))
		return container

	def parse_block(self, block):
		try:
			url_block = block.select_one('a.product-card__main.j-card-linc')
			url = url_block.get('href')
			return url
		except:
			return "Ошибка в блоке"


a = Client()
print(a.parse_page())
