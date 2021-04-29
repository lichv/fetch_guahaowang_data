from lichv.utils import *
from lichv.postgresqldb import PostgresqlDBService
import os
import hashlib
import urllib
import time

db = PostgresqlDBService.instance(host='localhost', port=5432, user='postgres', passwd='123456', db='new')

def getFilename(url, project = 'guahaowang', host='https://www.guahao.com/'):
	if url.startswith('https://www.guahao.com/help/docx') or url.startswith('https://www.guahao.com/search/expert') or url.startswith('https://www.guahao.com/expert'):
		url = handleURL(url)
		url = urllib.parse.unquote(url).encode('utf-8')
		filename = hashlib.md5(bytes(url)).hexdigest()+'.html'
	else:
		filename = handleURL(url)
	if filename.endswith('/'):
		filename = filename +  'index.html'
	else:
		if not filename.endswith('.html'):
			filename = filename +  '.html'
	filename = './'+project+'/'+filename[23:]
	return filename

def done(db,process):
	project = 'guahaowang'
	host = 'https://www.guahao.com/'
	filename = getFilename(process['name'],project,host)
	html = getHtml(process['name'])
	if not os.path.exists(filename):
		write(filename,html)
	links = getLinks(process['name'],html,[host])
	for link in links:
		print(link['link'])
		info = db.getOne('guahaowang',{'name':link['link']})
		if not info:
			db.add('guahaowang',{'name':link['link'],'label':'','value':'','flag':False,'state':False})
	db.modify('guahaowang',{'name':process['name']},{'flag':True})


process = db.getOne('guahaowang',{'flag':False,'state':False})
while process:
	print(process)
	db.modify('guahaowang',{'name':process['name']},{'state':True})
	time.sleep(3)
	done(db,process)
	process = db.getOne('guahaowang',{'flag':False,'state':False})
	

# db.add('guahaowang',{'name': 'https://www.guahao.com/s/子宫内膜息肉', 'label': '', 'value': '', 'flag': False, 'state': False})
# print(links)
# db.modify('guahaowang',{'name':link},{'flag':True})

# uri = 'https://www.guahao.com/department/9822d4bf-c720-11e1-913c-5cf9dd2e7135000?isStd='
# result = urllib.parse.urlparse(uri)
# url = result.scheme + '://' + result.netloc + result.path
# print(result)
# print(uri)
# print(url)
print('ok')