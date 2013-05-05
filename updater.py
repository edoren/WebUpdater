# -*- coding: utf-8 -*-

import os
import sys
import time

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
            self.localHashDict = hashgen.openHashDict(os.path.join(save_directory, 'updater.dat'))
        except Exception as exc:
            print(exc)
            self.localHashDict = {}

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

        self.serverHashDict = hashgen.openHashDict(self.downloadFile(config['FTP_Server']['HashPath']))
        # print(self.serverHashDict)

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
        finally:
            hashgen.saveHashDict(self.localHashDict, self.updaterDir)
            print(os.getcwd())
            self.ui.updateStatus = False
            time.sleep(0.5)
            print("Update Complete.")
            self.ui.statusLabel.setText("Update Complete.")

    def calculateDiffer(self):
        fileDiffer = DictDiffer(self.serverHashDict, self.localHashDict)
        # downloadDiffer(fileDiffer.added())
        # downloadDiffer(fileDiffer.changed())


    def downloadDiffer(self, differ_set):
        # for files in fileDiffer.added():
        #     print(files)
        pass

    def removeDiffer(self, differ_set):
        pass

    def getFullSize():
        pass

    def downloadFile(self, ftp_filepath):
        self.ui.statusText("Downloading")
        self.dl_file_size = 0
        self.pBarValue.set(0)
        self.file_size_bytes = self.host.path.getsize(ftp_filepath)
        self.file_size = self.__size(self.file_size_bytes)
        download_path, filename=self.host.path.split(ftp_filepath)
        print("Downloading " + filename + " - Size: " + self.file_size)
        self.ui.statusLabel2.setText(filename + " - Size:" + self.file_size)
        try:
            self.host.download(ftp_filepath, os.path.join(download_path, filename), mode='b', callback=self.__downloadBuffer)
        except OSError as exc:
            print(exc)
         
        return os.path.join(download_path, filename)

    def downloadFolderFiles(self, ftp_path=''):
        try:
            os.mkdir(ftp_path)
            print(ftp_path)
        except OSError:
            print("The folder", ftp_path, "already exist.")

        self.ui.startPBar(self.pBarValue)

        for filename in self.host.listdir(ftp_path):
            ftp_filepath = self.host.path.join(ftp_path, filename)
            print(ftp_filepath)

            if self.host.path.isfile(ftp_filepath):
                try:
                    localFileHash = hashgen.getFileHash(ftp_filepath)
                except Exception as e:
                    localFileHash = None
                    print("El archivo no existe.")

                if self.serverHashDict[ftp_filepath] != localFileHash:
                    self.downloadFile(ftp_filepath)

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
