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
        response = self.dbManager.insertIntoQuery('audio', 'filename, title, authorName, creds', f"{filename}, {title}, {authorName}, {creds}")
        return response

    def createThumbnail(self, filename, creds):
        response = self.dbManager.insertIntoQuery('image', 'filename, creds', f"{filename}, {creds}")
        return response
        
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
            videoTitle = f"'{audioFilename}'"

            audioCreds = audio[4]
            imageCreds = thumbnail[2]
            videoDescription = f"'{audioCreds}, {imageCreds}'"

            return videoTitle, videoDescription, audioID, thumbnailID
        else:
            return None

    def createVideo(self):
        try:
            videoTitle, videoDescription, audioID, thumbnailID = self.prepCreateVideo()
            self.dbManager.insertIntoQuery('video', 'audioID, thumbnailID, title, description', f'{audioID}, {thumbnailID}, {videoTitle}, {videoDescription}')
        except:
            pass
        
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

    def getAudiosRendered(self):
        response = self.dbManager.selectQuery('*', 'audio', 'rendered == true')
        return response

    def getAudioIDUnrendered(self):
        response = self.dbManager.selectLimit1Query('*', 'audio', 'rendered == false')
        if response:
            return response[0][0]
        else:
            return None

    def getThumbnailUnrendered(self):
        response = self.dbManager.selectLimit1Query('*', 'image', 'rendered == false')
        return response

    def getThumbnailsRendered(self):
        response = self.dbManager.selectQuery('*', 'image', 'rendered == true')
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

    def getVideosUploaded(self):
        response = self.dbManager.selectQuery('*', 'video', 'rendered == true AND uploaded == true')
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

    def checkIfAudioExists(self, title):
        response = self.dbManager.selectLimit1Query('*', 'audio', f'{title}')
        return bool(response)

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
            pass

    def createAudioFromResponse(self, title, response):
        filePath = f'{self.audioDir}/{title}.mp3'
        self.createFileFromBytes(response, filePath)

    def createPhotoFromResponse(self, title, response):
        filePath = f'{self.imageDir}/{title}.jpg'
        self.createFileFromBytes(response, filePath)
        self.formater.run(filePath)

    def createFileFromBytes(self, bytes, filePath):
        if not self.checkIfFileExists(filePath):
            self.createFile(filePath)
            try:
                with open(filePath, 'wb') as file:
                    for block in bytes.iter_content(1024):
                        if not block:
                            break

                        file.write(block)
            except:
                raise
            
    def checkIfFileExists(self, path):
        return os.path.isfile(path)

    def deleteFile(self, source):
        try:
            os.remove(source)
        except:
            raise
    
    def deleteUploadedFiles(self):
        audios = self.getAudiosRendered()
        images = self.getThumbnailsRendered()
        videos = self.getVideosUploaded()
        for audio in audios:
            try:
                if audio:
                    self.deleteFile(f"{self.audioDir}/'{audio[1]}'.mp3")
            except:
                pass

        for image in images:
            try:
                if image:
                    self.deleteFile(f'{self.imageDir}/{image[1]}.jpg')
            except:
                pass

        for video in videos:
            try:
                if video:
                    self.deleteFile(f'{self.videoDir}/{video[3]}.mp4')   
            except:
                pass
