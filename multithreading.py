from lichv.utils import *
from lichv.postgresqldb import PostgresqlDBService
import os
import hashlib
import urllib
import time
import threading



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

def hanle(db,process):
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

def done(db):
	process = db.getOne('guahaowang',{'flag':False,'state':False})
	while process:
		print(process)
		db.modify('guahaowang',{'name':process['name']},{'state':True})
		time.sleep(3)
		hanle(db,process)
		process = db.getOne('guahaowang',{'flag':False,'state':False})

class myThread (threading.Thread):
	def __init__(self, db, name):
		threading.Thread.__init__(self)
		self.db = db
		self.name = name
	def run(self):
		print ("开启线程：" + self.name)
		done(self.db)
		print ("退出线程：" + self.name)

db = PostgresqlDBService.instance(host='localhost', port=5432, user='postgres', passwd='123456', db='new')
for x in range(1,10):
	thread = myThread(db, str(x))
	thread.start()
print('ok')