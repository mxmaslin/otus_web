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

logging.basicConfig(filename='fetcher.log', level=logging.WARNING)


def get_parser():
	parser = argparse.ArgumentParser()
	parser.add_argument('--amount', nargs='?', type=int)
	parser.add_argument(
		'--recursive',
		nargs='?',
		type=lambda x: bool(strtobool(x)),
		default=False,
		const=False
		)
	parser.add_argument('--query', nargs='+', type=str)
	return parser


def get_parser_args():
	parser = get_parser()
	args = parser.parse_args()
	query = ' '.join(args.query)
	recursive = args.recursive
	links_amount = args.amount
	if not links_amount or links_amount <= 0:
		now = datetime.now().strftime('%Y.%m.%d %H:%M:%S')
		logging.warning(f'{now} Links amount must be > 0')
		exit()
	return query, links_amount, recursive


def fetch_hrefs_from_page(url):
	response = requests.get(url)
	soup = BeautifulSoup(response.text, 'html.parser')
	a_tags = soup.find_all('a', href=True)
	return [a['href'] for a in a_tags if validators.url(a['href'])]


def get_search_result(query, links_amount, recursive=None):
	search_result = search(query, stop=links_amount)
	return {
		i: {
			'url': url,
			'fetched': fetch_hrefs_from_page(url) if recursive else []
		}
		for i, url in enumerate(search_result, 1)
	}


def print_result(search_result):
	for result in sorted(search_result):
		print(f'# {result}: {unquote(search_result[result]["url"])}')
		if search_result[result]['fetched']:
			for url in search_result[result]['fetched']:
				print(f'\t{unquote(url)}')


def main():
	query, links_amount, recursive = get_parser_args()
	search_result = get_search_result(query, links_amount, recursive)
	print_result(search_result)


if __name__ == '__main__':
	try:
		main()
	except urllib.error.URLError:
		now = datetime.now().strftime('%Y.%m.%d %H:%M:%S')
		logging.warning(f'{now} No internet connection')
		exit()

