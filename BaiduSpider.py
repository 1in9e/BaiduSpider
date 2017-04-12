#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# __author__: 0h1in9e[https://www.ohlinge.cn]

import re
import sys
import time
import threading
import requests
import Queue
from bs4 import BeautifulSoup
from urlparse import urlparse

'''
ReadMe:
url: https://www.baidu.com/s?wd=[keywords]&pn=[pages]
parama:
	wd= 
	pn= 0～750 
'''

headers = {
		'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36'
}
# 定义多线程类 @BaiduSpider
class BaiduSpider(threading.Thread):
	def __init__(self, queue):
		threading.Thread.__init__(self)
		self._queue = queue

	def run(self):
		while not self._queue.empty():
			url = self._queue.get_nowait()
			try:
				self.spider(url)
			except Exception,e:
				print e

	def spider(self, url):
		r = requests.get(url, headers= headers)
		soup = BeautifulSoup(r.content,'html.parser')
		bd_urls = soup.find_all(name='a', attrs={'data-click':re.compile('.'), 'class':None})
 		for bd_url in bd_urls:
 			real_response = requests.get(bd_url['href'],headers=headers,timeout=5)
 			if real_response.status_code == 200:
 				domains = []
 				urls = []
 				# 得到搜索结果的真实URL
 				real_url = real_response.url
 				# Get domain name from url
 				parsed_uri = urlparse(real_url)
 				real_domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
 				# domain+url 去重
 				if real_domain not in domains:
 					domains.append(real_domain)
 					urls.append(real_url)
	 				with open('bd_url.txt','a') as ff:
	 					print "[+] %s Adding %s " % (time.strftime('%H:%M:%S'),real_url)
	 					ff.write(real_url+'\n')
	 				with open('bd_domain.txt','a') as f:
	 					print "[+] %s Adding %s " % (time.strftime('%H:%M:%S'),real_domain)
	 					f.write(real_domain+'\n')
 		
 				

def main(keyword):
	queue = Queue.Queue()
	url = "https://www.baidu.com/s?wd="+keyword+"&pn="
	for page in range(0,750,10):
		queue.put(url+str(page))
	threads = []
	# 线程数
	thread_count = 2

	for i in range(thread_count):
		threads.append(BaiduSpider(queue))
	for t in threads:
		t.start()
	for t in threads:
		t.join()

if __name__ == '__main__':
	if len(sys.argv) != 2:
		print "BaiduSpider from  keywords"
		print "Usage: %s 'keyword'" % sys.argv[0]
		print "Eg. BaiduSpider 'inurl:index.action'"
		print "Will make bd_url.txt AND bd_domain.txt"
		print "Author:0h1in9e[https://www.ohlinge.cn]"
	else:
		main(sys.argv[1])
