#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Python native libraries
import sys
import os
import threading
import hashlib
import pickle

# External libraries
import updater # import updater.py
from ui import Ui_Form # Call Ui_Form method from ui.py
from PyQt4 import QtCore, QtGui 

def sha1_hash(filepath):
    sha1 = hashlib.sha1()
    f = open(filepath, 'rb')
    try:
        sha1.update(f.read())
    finally:
        f.close()
    return sha1.hexdigest()

def checkHash():
	# updater.download("https://dl.dropboxusercontent.com/s/bvs6ndkmlm2a38n/hash_server.dat")
	
	hashDict = {}

	if os.name == 'posix':
		modsPath = os.getenv("HOME")+"/.minecraft/mods"
		binPath = os.getenv("HOME")+"/.minecraft/bin"
	elif os.name == 'windows':
		modsPath = os.getenv("APPDATA")+"\.minecraft\mods"
		binPath = os.getenv("APPDATA")+"\.minecraft\\bin"

	# files = [f for f in os.listdir(modsPath) if os.path.isfile(os.path.join(modsPath,f))]
	files = [ f for f in os.listdir(modsPath) if f.endswith(".jar") or f.endswith(".zip") ]

	hash_file = open('hash.dat', 'wb')
	for f in files:
		hashDict[f] = sha1_hash(modsPath + "/" + f)
	pickle.dump(hashDict, hash_file)
	hash_file.close()

	pkl_file = open('hash.dat', 'rb')
	mydict2 = pickle.load(pkl_file)
	pkl_file.close()

	print(hashDict)
	print(mydict2)

if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)
	Form = QtGui.QWidget()
	ui = Ui_Form()
	ui.setupUi(Form)
	Form.show()

	# self.statusCount = 0

	statusThread = threading.Thread( target=ui.windowStatus, args=( ) )
	checkHashThread = threading.Thread( target=checkHash, args=( ) )

	try:
		statusThread.setDaemon(True)
		checkHashThread.setDaemon(True)
		statusThread.start()
		checkHashThread.start()
	except:
		print("Error: unable to start thread")

	sys.exit(app.exec_())
