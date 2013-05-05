# -*- coding: utf-8 -*-

import os
import sys

import hashgen
from dictdiffer import DictDiffer

import ftputil

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
        self.updaterDir = os.getcwd()
        try:
            self.localHashDict = hashgen.openHashDict(os.path.join(self.updaterDir, 'updater.dat'))
        except Exception as exc:
            print(exc)
            self.localHashDict = {}

    def login(self, config):
        server = config['FTP_Server']['Server']
        username = config['FTP_Server']['Username']
        password = config['FTP_Server']['Password']
        self.serverpath = config['FTP_Server']['ServerFolder']
        self.download_path = config['DEFAULT']['DownloadPath']

        try:
            self.host = ftputil.FTPHost(server, username, password)
        except ftputil.ftp_error.PermanentError:
            self.ui.updateStatus = False
            print("Login authentication failed")
            self.ui.statusLabel2.setText("Login authentication failed")

        self.serverHashDict = hashgen.openHashDict(self.downloadFile(config['FTP_Server']['HashPath'], self.updaterDir))
        self.host.chdir(self.serverpath)
        # print(self.serverHashDict)

    def close(self):
        try:
            self.host.close()
        except:
            pass

    def downloadEntirePath(self):
        try:
            for (ftp_curpath, ftp_dirs, ftp_files) in self.host.walk(self.host.curdir):
                self.downloadFolderFiles(ftp_curpath)
        except Exception as exc:
            raise(exc)
        finally:
            hashgen.saveHashDict(self.localHashDict, self.updaterDir)

    def calculateDiffer(self):
        fileDiffer = DictDiffer(self.serverHashDict, self.localHashDict)
        self.downloadDiffer(fileDiffer.added())
        self.downloadDiffer(fileDiffer.changed())
        self.removeDiffer(fileDiffer.removed())

        hashgen.saveHashDict(self.localHashDict, self.updaterDir)

    def downloadDiffer(self, differ_set):
        for files in differ_set:
            self.downloadFile(files)
            self.localHashDict[files] = self.serverHashDict[files]

    def removeDiffer(self, differ_set):
        for files in differ_set:
            file_path = os.path.join(self.download_path, files)
            os.remove(file_path)
            del self.localHashDict[files]
            print("File", os.path.split(file_path)[1], "removed.")

    def getFullSize(self):
        pass

    def downloadFile(self, ftp_filepath, download_path):
        self.ui.statusText("Downloading")
        self.dl_file_size = 0
        self.pBarValue.set(0)
        self.file_size_bytes = self.host.path.getsize(ftp_filepath)
        self.file_size = self.__size(self.file_size_bytes)
        ftp_path, filename=self.host.path.split(ftp_filepath)
        print("Downloading " + filename + " - Size: " + self.file_size)
        self.ui.statusLabel2.setText(filename + " - Size:" + self.file_size)
        try:
            self.host.download(ftp_filepath, os.path.join(download_path, ftp_filepath), mode='b', callback=self.__downloadBuffer)
        except OSError as exc:
            print(exc)
         
        return os.path.join(download_path, filename)

    def downloadFolderFiles(self, ftp_path=''):
        try:
            os.mkdir(os.path.join(self.download_path, ftp_path))
            print(os.path.join(self.download_path, ftp_path))
        except OSError:
            print("The folder", ftp_path, "already exist.")

        self.ui.startPBar(self.pBarValue)

        for filename in self.host.listdir(ftp_path):
            ftp_filepath = self.host.path.join(ftp_path, filename)
            print(ftp_filepath)

            if self.host.path.isfile(ftp_filepath):
                try:
                    localFileHash = hashgen.getFileHash(os.path.join(self.download_path, ftp_filepath))
                except Exception as e:
                    localFileHash = None
                    print("The file doesn't exist.")

                if self.serverHashDict[ftp_filepath] != localFileHash:
                    self.downloadFile(ftp_filepath, self.download_path)

                self.localHashDict[ftp_filepath] = self.serverHashDict[ftp_filepath]
                    
        self.ui.stopPBar()

    def __downloadBuffer(self, buffer):
        self.dl_file_size += len(buffer)
        p = int(self.dl_file_size * 100 / self.file_size_bytes)
        self.pBarValue.set(p)

    def __size(self, size):
        if size < 1024:
            file_size = str("{0:.2f}".format(size)) + " Bytes"
        elif size/1024 < 1024:
            file_size = str("{0:.2f}".format(size/1024)) + " KB"
        else:
            file_size = str("{0:.2f}".format(size/1024**2)) + " MB"

        return file_size
