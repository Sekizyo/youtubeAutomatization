import os

from modules.storage.sqlManager import databaseManager
from modules.storage.formater import Formater

class FileManager():
    def __init__(self):
        self.dbManager = databaseManager()
        self.formater = Formater()

        self.audioDir = 'modules/storage/audio'
        self.imageDir = 'modules/storage/image'
        self.videoDir = 'modules/storage/video'

    def createAudio(self, filename, title, authorName, creds):
        self.dbManager.insertIntoQuery('audio', 'filename, title, authorName, creds, path', f'{filename}, {title}, {authorName}, {creds}')

    def createThumbnail(self, filename, creds):
        self.dbManager.insertIntoQuery('image', 'filename, creds', f"{filename}, {creds}")

    def prepCreateVideo(self):
        audioID = self.getAudioIDUnrendered()

        thumbnailID = self.getThumbnailIDUnrendered()

        if audioID and thumbnailID:
            audio = self.getAudioByID(audioID)[0]
            thumbnail = self.getThumbnailByID(thumbnailID)[0]


            self.updateAudioRenderStatusByID(audioID, True)
            self.updateThumbnailRenderStatusByID(thumbnailID, True)

            audioFilename = audio[1]
            audioAuthor = audio[3]
            videoTitle = audioFilename

            audioCreds = audio[4]
            imageCreds = thumbnail[2]
            videoDescription = f"'{audioCreds}, {imageCreds}'"

            return videoTitle, videoDescription, audioID, thumbnailID
        else:
            return None

    def createVideo(self):
        videoTitle, videoDescription, audioID, thumbnailID = self.prepCreateVideo()
        self.dbManager.insertIntoQuery('video', 'audioID, thumbnailID, title, description', f'{audioID}, {thumbnailID}, {videoTitle}, {videoDescription}')

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

    def getAudioIDUnrendered(self):
        response = self.dbManager.selectLimit1Query('*', 'audio', 'rendered == false')
        return response[0][0]

    def getThumbnailUnrendered(self):
        response = self.dbManager.selectLimit1Query('*', 'image', 'rendered == false')
        return response

    def getThumbnailIDUnrendered(self):
        response = self.dbManager.selectLimit1Query('*', 'image', 'rendered == false')
        return response[0][0]
        
    def getVideoUnrendered(self):
        response = self.dbManager.selectLimit1Query('*', 'video', 'rendered == false AND uploaded == false')
        return response

    def getVideoUnuploaded(self):
        response = self.dbManager.selectLimit1Query('*', 'video', 'rendered == true AND uploaded == false')
        return response

    def getVideoReady(self):
        video = self.getVideoUnuploaded()[0]
        if video:

            id_ = video[0]
            title = video[3]
            description = video[4]
            videoPath = f'{self.videoDir}/{title}.mp4'

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
        try:
            os.rename(source, destination)
            return True
        except:
            raise

    def createFile(self, path='modules/storage/'):
        try:
            file = open(path, "x")
            file.close()

        except:
            raise

    def createPhotoFromResponse(self, title, response):
        filePath = f'{self.imageDir}/{title}.jpg'
        self.createFile(filePath)

        with open(filePath, 'wb') as file:
            for block in response.iter_content(1024):
                if not block:
                    break

                file.write(block)

        self.formater.run(filePath)

    def checkIfFileExists(self, path):
        return os.path.isfile(path)

    def deleteFile(self, source):
        try:
            os.remove(source)
        except:
            raise