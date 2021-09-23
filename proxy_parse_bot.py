import requests
import json
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from time import sleep

with open('./config.json', 'r') as f:
	CONFIG = json.load(f)

URL = 'https://free-proxy-list.net/'

def bot_request(url):
	# bot_proxy = {
	# 	'http': f'http://{CONFIG["proxy"]["ip"]}:{CONFIG["proxy"]["port"]}',
	# 	'https': f'https://{CONFIG["proxy"]["ip"]}:{CONFIG["proxy"]["port"]}'
	# }
	bot_headers = {
		'user-agent': UserAgent().random,
		'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
		'accept-encoding': 'utf-8'
	}

	response = requests.get(url, headers=bot_headers)
	return response.text


def proxy_parse(text):
	proxies_list = []

	soup = BeautifulSoup(text, 'html.parser')
	proxy_table = soup.find('div', class_='fpl-list').find('table')
	proxies_table_body = proxy_table.find('tbody')

	for tr in proxies_table_body:
		td_s = tr.find_all('td')

		proxy_http = 'https://' if td_s[6].text == 'yes' else 'http://'
		proxy_ip = td_s[0].text
		proxy_port = td_s[1].text
		proxy = f'{proxy_http}{proxy_ip}:{proxy_port}'

		proxies_list.append(proxy)

	return proxies_list


def write_proxy(proxies_list, filepath):
	with open(filepath, 'w') as f:
		for proxy in proxies_list:
			f.write(proxy + '\n')


def bot_start(delay):
	while True:
		text = bot_request(URL)
		proxies_list = proxy_parse(text)
		write_proxy(proxies_list, CONFIG['output_file_path'])

		print('[INFO] Proxy file updated')
		sleep(CONFIG['parse_delay_seconds'])


if __name__ == '__main__':
	bot_start(CONFIG['parse_delay_seconds'])