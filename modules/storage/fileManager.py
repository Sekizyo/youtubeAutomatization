import os

from modules.storage.sqlManager import databaseManager

class FileManager():
    def __init__(self):
        self.dbManager = databaseManager()
        self.unusedDir = '/modules/storage/unused'
        self.workInProgressDir = '/modules/storage/workInProgress'
        self.uploadedDir = '/modules/storage/uploaded'
        self.unusedVideoDir = self.unusedDir + '/video'
        self.unusedImageDir = self.unusedDir + '/image'

    def getVideoByID(self, videoID):
        response = self.dbManager.selectQuery('*', 'videos', f'ID == {videoID}')
        return response

    def getUnuploadedVideo(self):
        response = self.dbManager.selectQuery('*', 'videos', 'uploaded = False AND rendered = True LIMIT 1')
        return response

    def getUnrenderedVideo(self):
        response = self.dbManager.selectQuery('*', 'videos', 'rendered = False AND uploaded = False LIMIT 1')
        return response

    def getVideoBasicInfo(self):
        response = self.getUnuploadedVideo()
        if response:
            formatedResponse = response[0]
            id_ = formatedResponse[0]
            title = formatedResponse[2]
            description = formatedResponse[3]
            videoPath = formatedResponse[6]

            return id_, title, description, videoPath
        else:
            return None

    def getReadyVideo(self):
        response = self.getVideoBasicInfo()
        if response:
            id_, title, description, videoPath = response
            self.updateVideoUploadStatus(id_, True)
            return title, description, videoPath
        else:
            return None

    def updateVideoUploadStatus(self, videoID, status):
        self.dbManager.updateRecordByIDQuery('videos', 'uploaded', status, videoID)

    def updateVideoRenderStatus(self, videoID, status):
        self.dbManager.updateRecordByIDQuery('videos', 'rendered', status, videoID)
    
    def updateVideoPath(self, videoID, path):
        self.dbManager.updateRecordByIDQuery('videos', 'localization', path, videoID)

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

    def createFile(self, path='modules/storage/'):
        try:
            file = open(path, "x")
            file.close()

        except:
            pass

    def checkIfFileExists(self, path):
        return os.path.isfile(path)

    def deleteFile(self, source):
        if os.path.exists(source):
            try:
                os.remove(source)
                return True

            except:
                raise
        else:
            return False