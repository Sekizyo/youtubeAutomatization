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

    def checkForUnuploadedVideos(self):
        result = self.dbManager.selectQuery('*', 'videos', 'uploaded = False')
        return bool(result)

    def checkForUnrenderedVideos(self):
        result = self.dbManager.selectQuery('*', 'videos', 'rendered = False')
        return bool(result)

    def checkForReadyVideos(self):
        result = self.dbManager.selectQuery('*', 'videos', 'uploaded = False AND rendered = True')
        return bool(result)

    def getBasicVideoInfo(self):
        id_, title, description, videoLocation = self.dbManager.selectQuery('id, title, description, path','videos', 'uploaded = False LIMIT 1')
        return id_, title, description, videoLocation

    def getReadyVideo(self):
        id_, title, description, videoLocation = self.getBasicVideoInfo()
        self.updateVideoUploadStatus(id_, True)
        return title, description, videoLocation

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