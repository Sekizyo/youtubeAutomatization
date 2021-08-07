import os

from modules.storage.sqlManager import databaseManager

class FileManager():
    def __init__(self):
        self.dbManager = databaseManager()
        self.uploadedDir = '/media/joseph/HDD1/Py_projects/youtubeAutomatization/modules/storage/uploaded'
        self.unusedDir = '/media/joseph/HDD1/Py_projects/youtubeAutomatization/modules/storage/unused'

    def updateVideoUploadStatus(self, videoID, status):
        self.dbManager.updateRecordByIDQuery('videos', 'uploaded', status, videoID)
    
    def updateVideoPath(self, videoID, path):
        self.dbManager.updateRecordByIDQuery('videos', 'localization', path, videoID)

    def moveFile(self, source, destination): # Move or rename file
        os.rename(source, destination)

    def __del__(self):
        del self.dbManager

