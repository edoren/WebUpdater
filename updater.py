# -*- coding: utf-8 -*-

import os
import sys
import time
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

    def login(self, config):
        server = config['FTP_Server']['Server']
        username = config['FTP_Server']['Username']
        password = config['FTP_Server']['Password']
        self.serverpath = config['FTP_Server']['ServerFolder']

        try:
            self.host = ftputil.FTPHost(server, username, password)
        except ftputil.ftp_error.PermanentError:
            self.ui.updateStatus = False
            print("Login authentication failed")
            self.ui.statusLabel2.setText("Login authentication failed")

    def close(self):
        try:
            self.host.close()
        except:
            pass

    def downloadEntirePath(self, download_path=''):
        os.chdir(download_path)
        try:
            self.host.chdir(self.serverpath)
            for (ftp_curpath, ftp_dirs, ftp_files) in self.host.walk(self.host.curdir):
                self.downloadFolderFiles(ftp_curpath)
        except Exception as exc:
            raise(exc)

    def getFullSize():
        pass

    def downloadFile():
        pass

    def downloadFolderFiles(self, path=''):
        try:
            os.mkdir(path)
        except OSError:
            print("The folder", path, "already exist.")

        self.ui.startPBar(self.pBarValue)
        for filename in self.host.listdir(path):
            filepath = self.host.path.join(path, filename)
            self.ui.statusText("Downloading")
            if self.host.path.isfile(filepath):
                self.dl_file_size = 0
                self.pBarValue.set(0)
                self.file_size_bytes = self.host.path.getsize(filepath)
                self.file_size = self.__size(self.file_size_bytes)                
                print("Downloading " + filename + " Size: " + self.file_size)
                self.ui.statusLabel2.setText(filename + " - Size:" + self.file_size)
                try:
                    self.host.download(filepath, os.path.join(path, filename), mode='b', callback=self.__downloadBuffer)
                except OSError as exc:
                    print(exc)

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
