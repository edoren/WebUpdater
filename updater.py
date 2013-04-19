# -*- coding: utf-8 -*-

import sys
import time
import urllib.request

from PyQt4 import QtCore, QtGui 

class updater():
	def __init__(self, arg):
		super(updater, self).__init__()
		self.arg = arg

def download(url):
	file_name = url.split('/')[-1]

	while True:
		try:
			download = urllib.request.urlopen(url)
		except:
			print("Error trying to download the file, please check your network connection.")
			print("Trying again in 5 seconds")
			time.sleep(5)
			continue
		break

	file_save = open(file_name, 'wb')

	meta = download.info()

	file_size_bytes = int(meta['Content-Length'])

	if file_size_bytes < 1024:
		print_file_size = str("{0:.2f}".format(file_size_bytes)) + "Bytes"
	elif file_size_bytes/1024 < 1024:
		print_file_size = str("{0:.2f}".format(file_size_bytes/1024)) + "KB"
	else:
		print_file_size = str("{0:.2f}".format(file_size_bytes/1024**2)) + "MB"

	print("Downloading: {0} Size: {1}".format(file_name, print_file_size))

	dl_file_size = 0
	block_sz = 8192
	while True:
	    buffer = download.read(block_sz)
	    if not buffer:
	        break

	    dl_file_size += len(buffer)
	    file_save.write(buffer)
	    p = int(dl_file_size * 100 / file_size_bytes)
	    print(p)

	file_save.close()
