import requests
from bs4 import BeautifulSoup

url = "https://www.cricbuzz.com"
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html5lib')
table = soup.find_all('li', attrs = {'class': 'cb-col cb-col-25 cb-mtch-blk cb-vid-sml-card-api videos-carousal-item cb-carousal-item-large cb-view-all-ga'})

for each in table:
	match = each.text.strip()
	link = each.find('a', attrs = {'class': 'cb-font-12'})
	url2 = url + link['href']
	results = requests.get(url2)
	soups = BeautifulSoup(results.content, 'html5lib')
	stats = soups.find('div', attrs = {'class': 'cb-col-67 cb-col'})
	if stats:
		scores = stats.find_all('div')
		table = []
		itr = 0
		row = {}
		for each in scores:
			if(itr % 6 == 0 and len(row)):
				table.append(row)
				row = {}
			if(len(each.find_all('div'))==0):
				itr += 1
				row[(itr-1)%6] = each.text.strip()
			table.append(row)
for each in table:
	if each in table:
		table.remove(each)

for every in table:
	print(every[0], every[1], every[2], every[3], every[4], every[5])
#stats = soup.find('div', attrs = {'class': 'cb-col-67 cb-col'})
#scores = stats.find_all('div')
#print(stats)
#stats = soup.find('div', attrs = {'class': 'cb-col-67 cb-colcb-col-67 cb-colcb-col cb-col-25 cb-mtch-blk cb-vid-sml-card-api videos-carousal-item cb-carousal-item-large cb-view-all-ga'})
#scores = stats.find_all('div')

#print(stats)

