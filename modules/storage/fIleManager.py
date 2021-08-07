import os

from modules.storage.sqlManager import databaseManager

class FileManager():
    def __init__(self):
        self.dbManager = databaseManager()
        self.fileMover = FileMover()
        self.unusedDir = '/media/joseph/HDD1/Py_projects/youtubeAutomatization/modules/storage/unused'
        self.workInProgressDir = '/media/joseph/HDD1/Py_projects/youtubeAutomatization/modules/storage/workInProgress'
        self.uploadedDir = '/media/joseph/HDD1/Py_projects/youtubeAutomatization/modules/storage/uploaded'
        self.unusedVideoDir = self.unusedDir + '/video'
        self.unusedImageDir = self.unusedDir + '/image'

    def updateVideoUploadStatus(self, videoID, status):
        self.dbManager.updateRecordByIDQuery('videos', 'uploaded', status, videoID)
    
    def updateVideoPath(self, videoID, path):
        self.dbManager.updateRecordByIDQuery('videos', 'localization', path, videoID)
    

    def __del__(self):
        del self.dbManager
        del self.fileMover

class FileMover(FileManager):
    def __init__(self):
        super().__init__()
  
    def moveFileToUnused(self, source, video=True):
        if video:
            self.moveFile(source, self.unusedVideoDir)
        else:
            self.moveFile(source, self.unusedImageDir)

    def moveFileToWorking(self, source):
        self.moveFile(source, self.workInProgressDir)

    def moveFileToUploaded(self, source):
        self.moveFile(source, self.uploadedDir)

    def moveFile(self, source, destination):
        if os.path.exists(source) and os.path.exists(destination):
            try:
                os.rename(source, destination)
                return True

            except:
                raise
        else:
            return False

    def deleteFile(self, source):
        if os.path.exists(source):
            try:
                os.remove(source)
                return True

            except:
                raise
        else:
            return False