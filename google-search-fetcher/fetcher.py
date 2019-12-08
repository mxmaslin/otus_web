import argparse
import logging
import requests
import validators
import urllib

from datetime import datetime
from distutils.util import strtobool
from urllib.parse import unquote
from bs4 import BeautifulSoup
from googlesearch import search


def get_parser():
	parser = argparse.ArgumentParser()
	parser.add_argument('--amount', nargs='?', type=int, default=10, const=10)
	parser.add_argument(
		'--recursive',
		nargs='?',
		type=lambda x: bool(strtobool(x)),
		default=False,
		const=False
		)
	parser.add_argument('--query', nargs='+', type=str)
	return parser


def fetch_hrefs_from_page(url):
	response = requests.get(url)
	soup = BeautifulSoup(response.text, 'html.parser')
	a_tags = soup.find_all('a', href=True)
	hrefs = [a['href'] for a in a_tags if validators.url(a['href'])]
	return hrefs
	

def main():
	parser = get_parser()
	args = parser.parse_args()

	recursive = args.recursive
	if recursive in [0, False, '0', 'False', 'None']:
		recursive = False 

	query = ' '.join(args.query)
	links_amount = args.amount

	logging.basicConfig(filename='fetcher.log', level=logging.WARNING)
	if links_amount <= 0:
		now = datetime.now().strftime('%Y.%m.%d %H:%M:%S')
		logging.warning(f'{now} Links amount must be > 0')
		exit()

	search_result = search(query, stop=links_amount)

	for i, url in enumerate(search_result, 1):
		print(f'# {i}: {unquote(url)}')

		if recursive:
			fetched_hrefs = fetch_hrefs_from_page(url)
			if fetched_hrefs:
				print('\tСсылки на странице, куда ведёт этот url:')
				for href in fetch_hrefs_from_page(url):
					print(f'\t\t{unquote(href)}')


if __name__ == '__main__':
	try:
		main()
	except urllib.error.URLError:
		now = datetime.now().strftime('%Y.%m.%d %H:%M:%S')
		logging.warning(f'{now} No internet connection')
		exit()

