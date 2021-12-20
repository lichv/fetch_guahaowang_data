from lichv.utils import *
from lichvPy3mysql.mysqldb import MysqlDBService
import os
import hashlib
import urllib
import time

db = MysqlDBService(host='localhost', port=3306, user='root', passwd='123456', db='work')

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
	filename = getFilename(process['link'],project,host)
	html = getHtml(process['link'])
	if not os.path.exists(filename):
		write(filename,html)
	links = getLinks(process['link'],html,[host])
	for link in links:
		print(link['link'])
		info = db.getOne('guahaowang',{'link':link['link']})
		if not info:
			db.add('guahaowang',{'link':link['link'],'flag':0,'state':0,'created_at':time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),'updated_at':time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())})
	db.modify('guahaowang',{'link':process['link']},{'flag':1,'updated_at':time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())})


process = db.getOne('guahaowang',{'flag':0,'state':0})
while process:
	print(process)
	db.modify('guahaowang',{'link':process['link']},{'state':1})
	time.sleep(3)
	done(db,process)
	process = db.getOne('guahaowang',{'flag':0,'state':0})
	

print('ok')