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

    def createAudio(self, title, creds, path):
        try:
            self.dbManager.insertIntoQuery('audio', 'title, creds, path', f'{title}, {creds}, {path}')
        except:
            raise

    def createThumbnail(self, creds, path):
        try:
            self.dbManager.insertIntoQuery('thumbnail', 'creds, path', f'{creds}, {path}')
        except:
            raise

    def createVideo(self):
        audio = self.getAudioUnrendered()
        thumbnail = self.getThumbnailUnrendered()
        path = self.workInProgressDir

        try:
            audioID = audio[0]
            thumbnailID = thumbnail[0]

            self.updateAudioRenderStatusByID(audioID, True)
            self.updateThumbnailRenderStatusByID(thumbnailID, True)


            self.dbManager.insertIntoQuery('video', 'audioID, thumbnailID, path', f'{audioID}, {thumbnailID}, {path}')
        except:
            raise

    def getAudioByID(self, videoID):
        response = self.dbManager.selectQuery('*', 'audio', f'ID == {videoID}')
        return response

    def getThumbnailByID(self, videoID):
        response = self.dbManager.selectQuery('*', 'thumbnail', f'ID == {videoID}')
        return response

    def getVideoByID(self, videoID):
        response = self.dbManager.selectQuery('*', 'video', f'ID == {videoID}')
        return response

    def getAudioUnrendered(self):
        response = self.dbManager.selectLimit1Query('*', 'audio', 'rendered == false')
        return response

    def getThumbnailUnrendered(self):
        response = self.dbManager.selectLimit1Query('*', 'thumbnail', 'rendered == false')
        return response
        
    def getVideoUnuploaded(self):
        response = self.dbManager.selectLimit1Query('*', 'video', 'uploaded == false')
        return response

    def getVideoReady(self):
        response = self.getVideoUnuploaded()
        if response:
            formatedResponse = response[0]

            id_ = formatedResponse[0]
            title = formatedResponse[1]
            description = formatedResponse[2]
            videoPath = formatedResponse[3]

            self.updateVideoUploadStatusByID(id_, True)

            return title, description, videoPath
        else:
            return None

    def updateAudioRenderStatusByID(self, audioID, status):
        self.dbManager.updateRecordByIDQuery('audio', 'rendered', str(status).lower(), audioID)

    def updateThumbnailRenderStatusByID(self, thumbnailID, status):
        self.dbManager.updateRecordByIDQuery('thumbnail', 'rendered', str(status).lower(), thumbnailID)

    def updateVideoUploadStatusByID(self, videoID, status):
        self.dbManager.updateRecordByIDQuery('video', 'uploaded', str(status).lower(), videoID)

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