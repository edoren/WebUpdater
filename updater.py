# -*- coding: utf-8 -*-

import os
import sys
import time
import ftputil

from PyQt4 import QtCore, QtGui 

class Reference():
    def __init__(self, value):
        self.value = value
    def set(self, value):
        self.value = value
    def get(self):
        return self.value

class updater():
	def __init__(self, ui):
		super(updater, self).__init__()
		self.pBarValue = Reference(0)
		self.ui = ui

	def login(self, config):
		server = config['FTP']['server']
		username = config['FTP']['username']
		password = config['FTP']['password']

		self.host = ftputil.FTPHost(server, username, password)

	def close(self):
		self.host.close()

	def downloadFolderFiles(self, directory):
		self.ui.startPBar(self.pBarValue)

		for filename in self.host.listdir(self.host.curdir):
			if self.host.path.isfile(filename):
				self.dl_file_size = 0
				self.pBarValue.set(0)
				self.file_size_bytes = self.host.path.getsize(filename)
				print('Getting ' + filename + ' Size: ' + self.__size(self.file_size_bytes))
				self.host.download(filename, filename, mode='b', callback=self.__downloadBuffer)

		self.ui.stopPBar()

	def __downloadBuffer(self, buffer):
		self.dl_file_size += len(buffer)
		p = int(self.dl_file_size * 100 / self.file_size_bytes)
		self.pBarValue.set(p)
		print(p)

	def __size(self, size):
		if size < 1024:
			file_size = str("{0:.2f}".format(size)) + " Bytes"
		elif size/1024 < 1024:
			file_size = str("{0:.2f}".format(size/1024)) + " KB"
		else:
			file_size = str("{0:.2f}".format(size/1024**2)) + " MB"

		# print("File size: {0}".format(file_size))

		return file_size
