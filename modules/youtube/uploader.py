import os
import datetime
from datetime import time

from googleapiclient.http import MediaFileUpload

class YoutubeUploader():
    def __init__(self, youtube, fileManager):
        self.youtube = youtube
        self.fileManager = fileManager

        self.categoryId = 10 # Music
        self.videoDir = '/media/joseph/HDD1/Py_projects/youtubeAutomatization/modules/storage/workInProgress'

    def createTitleDefault(self, videoTitle):
        songName, authorName = str(videoTitle).split(' - ')

        return f'{songName} - {authorName} - beats to relax/study to'

    def createDescriptionDefault(self, creds):
        return f"Thank you for listening, I hope you will have a good time\nCredits:\n–––––––––––––––––––––––––––––– \n{creds}\n ––––––––––––––––––––––––––––––"

    def getUploadTime(self):
        format = "%d-%m-%Y"

        now = datetime.datetime.now()
        now_date = now.strftime("%d-%m-%Y")

        start_date = now.strptime(now_date, format)
        start_date = start_date + datetime.timedelta(minutes=10)

        start_date = start_date.isoformat() + "Z"
        return start_date

    def upload(self):
        video = self.fileManager.getReadyVideo()
        if video:
            videoTitle, videoDescription, videoPath = video

            title = self.createTitleDefault(videoTitle)
            description = self.createDescriptionDefault(videoDescription)

            response = self.uploadRequest(title, description, videoPath)
        else:
            print('Upload failed, file not found')

    def uploadRequest(self, title, description, videoPath):
        request_body = {
            'snippet': {
                'categoryID': self.categoryId,
                'title': title,
                'description': description,
            },
            'status': {
                'privacyStatus': 'private',
                'publishAt': self.getUploadTime(),
                'selfDeclaredMadeForKids': False, 
            },
            'notifySubscribers': False
        }
        mediaFile = MediaFileUpload(videoPath)


        print('########## upload started ##########')
        response_upload = self.youtube.videos().insert(
            part='snippet,status',
            body=request_body,
            media_body=mediaFile
        ).execute()

        return response_upload
