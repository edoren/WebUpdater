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

def getHash(rootpath):
    hashDict = {}

    for (path, dirs, files) in os.walk(rootpath):
        for filename in files:
            hashDict[os.path.join(path, filename).split(rootpath)[1]] = __sha1_hash(os.path.join(path, filename))
            print(os.path.join(path, filename).split(rootpath)[1])
    
    hash_file = open('updater.dat', 'wb')
    pickle.dump(hashDict, hash_file)
    hash_file.close()

    # pkl_file = open('updater.dat', 'rb')
    # mydict2 = pickle.load(pkl_file)
    # pkl_file.close()

    print(hashDict)

def main(rootpath):
    getHash(rootpath)

if __name__ == '__main__':
    try:
        rootpath = sys.argv[1]
        main(rootpath)
    except:
        print("Falta un argumento")
