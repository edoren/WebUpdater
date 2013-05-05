# -*- coding: utf-8 -*-

import os
import sys
import hashlib
import pickle

def __sha1_hash(filepath):
    sha1 = hashlib.sha1()
    f = open(filepath, 'rb')
    try:
        sha1.update(f.read())
    finally:
        f.close()
    return sha1.hexdigest()

def getFileHash(file_path):
    return __sha1_hash(file_path)

def openHashDict(data_file):
    pkl_file = open(data_file, 'rb')
    hashdict = pickle.load(pkl_file)
    pkl_file.close()
    return hashdict

def saveHashDict(hash_dict, save_directory=''):
    hash_file = open(os.path.join(save_directory, 'updater.dat'), 'wb')
    pickle.dump(hash_dict, hash_file)
    hash_file.close()
