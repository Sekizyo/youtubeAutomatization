import os

from modules.storage.sqlManager import databaseManager

class FileManager():
    def __init__(self):
        self.dbManager = databaseManager()

        self.audioDir = 'modules/storage/audio'
        self.imageDir = 'modules/storage/image'
        self.videoDir = 'modules/storage/video'

    def createAudio(self, title, creds, path):
        try:
            self.dbManager.insertIntoQuery('audio', 'title, creds, path', f'{title}, {creds}, {path}')
        except:
            raise

    def createThumbnail(self, filename, creds):
        try:
            self.dbManager.insertIntoQuery('image', 'filename, creds', f"{filename}, {creds}")
        except:
            raise

    def createVideo(self):
        audio = self.getAudioUnrendered()
        thumbnail = self.getThumbnailUnrendered()
        path = self.videoDir

        try:
            audioID = audio[0]
            thumbnailID = thumbnail[0]

            self.updateAudioRenderStatusByID(audioID, True)
            self.updateThumbnailRenderStatusByID(thumbnailID, True)

            title = audio[1]

            self.dbManager.insertIntoQuery('video', 'audioID, thumbnailID, title, path', f'{audioID}, {thumbnailID}, {title}, {path}')
        except:
            raise

    def getAudioByID(self, videoID):
        response = self.dbManager.selectQuery('*', 'audio', f'ID == {videoID}')
        return response

    def getThumbnailByID(self, videoID):
        response = self.dbManager.selectQuery('*', 'image', f'ID == {videoID}')
        return response

    def getVideoByID(self, videoID):
        response = self.dbManager.selectQuery('*', 'video', f'ID == {videoID}')
        return response

    def getAudioUnrendered(self):
        response = self.dbManager.selectLimit1Query('*', 'audio', 'rendered == false')
        return response

    def getThumbnailUnrendered(self):
        response = self.dbManager.selectLimit1Query('*', 'image', 'rendered == false')
        return response
        
    def getVideoUnrendered(self):
        response = self.dbManager.selectLimit1Query('*', 'video', 'rendered == false AND uploaded == false')
        return response

    def getVideoUnuploaded(self):
        response = self.dbManager.selectLimit1Query('*', 'video', 'rendered == true AND uploaded == false')
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
        self.dbManager.updateRecordByIDQuery('image', 'rendered', str(status).lower(), thumbnailID)

    def updateVideoRenderStatusByID(self, videoID, status):
        self.dbManager.updateRecordByIDQuery('video', 'rendered', str(status).lower(), videoID)

    def updateVideoUploadStatusByID(self, videoID, status):
        self.dbManager.updateRecordByIDQuery('video', 'uploaded', str(status).lower(), videoID)

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

    def createPhotoFromResponse(self, title, response):
        filePath = f'{self.imageDir}/{title}.jpg'
        self.createFile(filePath)

        with open(filePath, 'wb') as file:
            for block in response.iter_content(1024):
                if not block:
                    break

                file.write(block)

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