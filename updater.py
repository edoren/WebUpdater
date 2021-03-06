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
        self.pBar1Value = Reference(0)
        self.pBar2Value = Reference(0)
        self.totalDownSize = 0
        self.ui = ui
        self.updaterDir = os.getcwd()
        try:
            self.localHashDict = hashgen.openHashDict(os.path.join(self.updaterDir, 'updater.dat'))
        except IOError as exc:
            # print(exc)
            self.localHashDict = {}

    def login(self, config):
        server = config['FTP_Server']['Server']
        username = config['FTP_Server']['Username']
        password = config['FTP_Server']['Password']
        self.serverpath = config['FTP_Server']['ServerFolder']
        self.download_path = config['DEFAULT']['DownloadPath']

        try:
            self.host = ftputil.FTPHost(server, username, password)
            print("Conection Started")
            self.serverHashDict = hashgen.openHashDict(self.downloadFile(config['FTP_Server']['HashPath'], self.updaterDir))
            self.ui.statusLabel2.setText("")
            self.fileDiffer = DictDiffer(self.serverHashDict, self.localHashDict)
            self.host.chdir(self.serverpath)
        except ftputil.ftp_error.PermanentError:
            print("Error!")
            print("Login authentication failed.")
            self.ui.statusLabel.setText("Error!")
            self.ui.statusLabel2.setText("Login authentication failed.")
            return 0
        except ftputil.ftp_error.FTPOSError as error:
            print("Error!")
            print("No Internet connection.")
            self.ui.statusLabel.setText("Error!")
            self.ui.statusLabel2.setText("No Internet connection.")
            # raise(error)
            return 0

        self.pBar1Value.set(0)
        self.pBar2Value.set(0)

    def close(self):
        try:
            self.host.close()
            print("\nConection Closed")
            return 0
        except:
            pass

    def checkDownloadPath(self, download_path):
        if not os.path.exists(download_path):
            try:
                os.makedirs(download_path)
            except Exception as exc:
                print(exc)

    def downloadEntirePath(self):
        self.totalSize = self.getFullSize()
        try:
            for (ftp_curpath, ftp_dirs, ftp_files) in self.host.walk(self.host.curdir):
                self.downloadFolderFiles(ftp_curpath)
            hashgen.saveHashDict(self.localHashDict, self.updaterDir)
        except Exception as exc:
            raise(exc)

    def checkDiffer(self):
        if len(self.fileDiffer.added()) != 0 or len(self.fileDiffer.changed()) != 0 or len(self.fileDiffer.removed()) != 0 or not os.path.exists(self.download_path):
            return True
        else:
            return False

    def calculateDiffer(self):
        if os.path.exists(os.path.join(self.updaterDir, 'updater.dat')) and os.path.exists(self.download_path):
            self.downloadDiffer(self.fileDiffer.added())
            self.downloadDiffer(self.fileDiffer.changed())
            self.removeDiffer(self.fileDiffer.removed())
            hashgen.saveHashDict(self.localHashDict, self.updaterDir)
        else:
            try:
                try:
                    os.remove(os.path.join(self.updaterDir, 'updater.dat'))
                except:
                    pass
                self.downloadEntirePath()
            except Exception as exc:
                raise(exc)
                os.remove(os.path.join(self.updaterDir, 'updater.dat'))


    def downloadDiffer(self, differ_set):
        for files in differ_set:
            self.downloadFile(files, self.download_path)
            self.localHashDict[files] = self.serverHashDict[files]

    def removeDiffer(self, differ_set):
        for files in differ_set:
            file_path = os.path.join(self.download_path, files)
            os.remove(file_path)
            del self.localHashDict[files]
            print("File", os.path.split(file_path)[1], "removed.")

    def getFullSize(self):
        totalSize = 0
        for (ftp_curpath, ftp_dirs, ftp_files) in self.host.walk(self.host.curdir):
            for files in ftp_files:
                totalSize += self.host.path.getsize(self.host.path.join(ftp_curpath, files))
        return(totalSize)

    def downloadFile(self, ftp_filepath, download_path):
        self.ui.statusText = "Downloading"
        self.dl_file_size = 0
        self.pBar1Value.set(0)
        self.file_size_bytes = self.host.path.getsize(ftp_filepath)
        file_size = self.__size(self.file_size_bytes)
        ftp_path, filename=self.host.path.split(ftp_filepath)
        print("\nDownloading " + filename + " - Size: " + file_size)
        self.ui.statusLabel2.setText(filename + " - Size:" + file_size)
        try:
            self.checkDownloadPath(os.path.join(download_path, ftp_path))
            self.host.download(ftp_filepath, os.path.join(download_path, ftp_filepath), mode='b', callback=self.__downloadBuffer)
            print(end="\n\n")
        except OSError as exc:
            raise(exc)
         
        return os.path.join(download_path, filename)

    def downloadFolderFiles(self, ftp_path=''):
        self.ui.startPBars(self.pBar1Value, self.pBar2Value)

        for filename in self.host.listdir(ftp_path):
            ftp_filepath = self.host.path.join(ftp_path, filename)
            # print(ftp_filepath)

            if self.host.path.isfile(ftp_filepath):
                self.ui.updateStatus = True
                self.ui.statusText = "Checking files"
                self.ui.statusLabel2.setText("Checking " + filename)
                print("Checking", filename)
                try:
                    localFileHash = hashgen.getFileHash(os.path.join(self.download_path, ftp_filepath))
                except Exception as exc:
                    localFileHash = None

                if self.serverHashDict[ftp_filepath] != localFileHash:
                    self.downloadFile(ftp_filepath, self.download_path)
                else:
                    self.totalDownSize += self.host.path.getsize(ftp_filepath)
                    self.pBar2Value.set(int(self.totalDownSize * 100 / self.totalSize))

                self.localHashDict[ftp_filepath] = self.serverHashDict[ftp_filepath]
                    
        self.ui.stopPBars()

    def __downloadBuffer(self, buffer):
        buffer_len = len(buffer)
        self.dl_file_size += buffer_len
        self.totalDownSize += buffer_len
        p = int(self.dl_file_size * 100 / self.file_size_bytes)
        try:
            r = int(self.totalDownSize * 100 / self.totalSize)
        except:
            r = int(self.totalDownSize * 100 / self.file_size_bytes)
        print("Status: ", p, "%", end="\r")
        self.pBar1Value.set(p)
        self.pBar2Value.set(r)        

    def __size(self, size):
        if size < 1024:
            file_size = str("{0:.2f}".format(size)) + " Bytes"
        elif size/1024 < 1024:
            file_size = str("{0:.2f}".format(size/1024)) + " KB"
        elif size/1024**2 < 1024:
            file_size = str("{0:.2f}".format(size/1024**2)) + " MB"
        elif size/1024**3 < 1024:
            file_size = str("{0:.2f}".format(size/1024**3)) + " GB"

        return file_size
