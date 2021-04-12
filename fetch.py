from lichv.utils import *
from lichv.postgresqldb import PostgresqlDBService
import os
import urllib
import time

db = PostgresqlDBService.instance(host='localhost', port=5432, user='postgres', passwd='123456', db='new')

host = 'https://www.guahao.com/s/%E8%80%B3%E8%81%8B/eteam/3/%E5%A4%A9%E6%B4%A5/3358/%E5%8C%97%E8%BE%B0%E5%8C%BA'
page = db.getOne('guahaowang',{'flag':False,'state':False})
# if page :
while page :
	uri = page['name']
	temp = urllib.parse.urlparse(uri)
	uri = temp[0]+'://'+temp[1]+temp[2]
	db.modify('guahaowang',{'name':uri},{'state':True})
	html = getHtml(uri)

	if uri.endswith('/'):
		uri = uri +  'index.html'
	else:
		if not uri.endswith('.html'):
			uri = uri +  '.html'
	filename = './guahaowang'+uri[22:]
	filename = filename.replace('/','\\')
	filename = urllib.parse.unquote(filename)
	if not os.path.exists(filename):
		write(filename,html)
	soup = BeautifulSoup(html,"html.parser")
	for link in soup.find_all('a'):
		href = link.get('href')
		text = link.text
		text = text.strip()
		new_full_url = urllib.parse.unquote(urllib.parse.urljoin(uri, href))
		result = urllib.parse.urlparse(new_full_url)
		trueUrl = result[0]+'://'+result[1]+result[2]
		if trueUrl.startswith('https://www.guahao.com/'):
			print(trueUrl)
			info = db.getOne('guahaowang',{'name':trueUrl})
			if not info:
				db.add('guahaowang',{'name':trueUrl,'label':text,'value':'','flag':False,'state':False})
	db.modify('guahaowang',{'name':uri},{'flag':True})
	page = db.getOne('guahaowang',{'flag':False,'state':False})

print('ok')