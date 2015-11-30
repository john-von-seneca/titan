

import requests
from bs4 import BeautifulSoup
import re
import pycurl

def extract_href_lang(td_a1):
	href = str(td_a1.contents[1]).split('\n')[0]
	href = href[9:-2]
	lang = td_a1.contents[1].contents[1].string.strip()
	return {'href': href, 'lang': lang}

def filter_lang(href_langs, lang):
	pattern = '.*'+lang+'.*'
	return [href_lang for href_lang in href_langs if re.search(pattern, href_lang['lang'], re.IGNORECASE)]

def download_link(dwld_link, folder):
	# todo
	c = pycurl.Curl()
	c.setopt(c.URL, 'http://libgen.io/get.php?md5='+md5_hash)
	c.setopt(c.FOLLOWLOCATION, True)
	c.setopt(c.WRITEDATA, f)
	c.perform()
	status = 'Status: %d' % c.getinfo(c.RESPONSE_CODE)
	c.close()

movie_name = 'departures'
url_root = 'http://subscene.com'
lang = 'English'
url = url_root + '/subtitles/title?q={0}&l='.format(movie_name)
response = requests.get(url)

bsoup = BeautifulSoup(response.text, 'lxml')


# find the div of search results
divs = [div for div in bsoup.findAll('div')]
divs_title = [div for div in divs if 'class' in div.attrs and 'title' in div.attrs['class']]
print(divs_title)

# for now, get the first div and again extract the contents
url_relative = divs_title[0].contents[1].attrs['href']
url = url_root + url_relative
response = requests.get(url)
bsoup2 = BeautifulSoup(response.text, 'lxml')
tds = bsoup2.findAll('td')
tds_a1 = [td for td in tds if 'class' in td.attrs and 'a1' in td.attrs['class']]
# contents if
href_langs = [extract_href_lang(td_a1) for td_a1 in tds_a1]
href_langs_en = filter_lang(href_langs, lang)

for ix, href_lang in enumerate(href_langs_en):
	href0 = href_lang['href']
	url = url_root + href0
	response = requests.get(url)
	bsoup3 = BeautifulSoup(response.text, 'lxml')
	links = bsoup3.findAll('a')
	dwld_links = [link for link in links if 'id' in xx.attrs]

	href1 = dwld_links[0].attrs['href']
	download_link(url_root + href1, '/home/dragon/Downloads/subtitles/{0}-{1}')
	

