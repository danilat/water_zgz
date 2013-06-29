import urllib2
import mechanize
import json
from bs4 import BeautifulSoup
import utm

browser = mechanize.Browser()
def parse(link):
	resp = browser.open(link)
	soup = BeautifulSoup(resp.read())
	title = soup.find('h2').text
	ele = soup.find('div', class_='elementos')
	divs = ele.find_all('div')
	for div in divs:
		pass
		#print div.text

	trs = ele.find('table').find_all('tr')
	trs.pop(0)

	indicators = []
	category = ""
	for tr in trs:
		has_category = tr.find('strong')
		if has_category:
			category = has_category.text
		else:
			metric = {'name': tr.find('td',  attrs={"headers": "nom"}).text, 
			'result': tr.find('td',  attrs={"headers": "res"}).text,
			'category': category}
			indicators.append(metric)
	return indicators


response = urllib2.urlopen('http://www.zaragoza.es/georref/json/hilo/ver_IMSP')
data = json.load(response)
features = data['features']
deposits = []
for feature in features:	
	
	deposit = {}
	deposit['title'] = feature['properties']['title']
	deposit['description'] = feature['properties']['description']
	deposit['date'] = feature['properties']['date']
	deposit['link'] = feature['properties']['link']
	deposit['indicators'] = parse(feature['properties']['link'])
	where = utm.to_latlon(feature['geometry']['coordinates'][0],feature['geometry']['coordinates'][1], 30, 'U')
	deposit['position'] = where
	deposits.append(deposit)

f = open('water_zgz.json', 'w')
f.write(json.dumps(deposits))
f.close()


