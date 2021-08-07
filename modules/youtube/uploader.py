import os

from googleapiclient.http import MediaFileUpload

class YoutubeUploader():
    def __init__(self, youtube):
        self.youtube = self.auth()

        self.scopes = ["https://www.googleapis.com/auth/youtube.upload"]
        self.api_service_name = "youtube"
        self.api_version = "v3"
        self.client_secrets_file = "client_secret.json"

        self.categoryId = 10 # Music
        self.videoDir = '/media/joseph/HDD1/Py_projects/youtubeAutomatization/modules/storage/workInProgress'

    def getTitle(self, videoTitle):
        songName, authorName = videoTitle.split(' - ')

        return f'{songName} - {authorName} - beats to relax/study to'

    def getDescription(self, creds):
        return f"Thank you for listening, I hope you will have a good time\nCredits:\n–––––––––––––––––––––––––––––– \n{creds}\n ––––––––––––––––––––––––––––––"

    def getVideoLocation(self, videoName):
        return f'{self.videoDir}/{videoName}'

    def getVideoTitle(self):
        result = os.system(f'ls {self.videoDir}/*.mp4 | head -1')

    def upload(self, title, description, videoLocation):
        videoTitle = self.getVideoTitle()

        title = self.generateTitle(videoTitle)
        description = self.generateDescription()
        videoLocation = self.getVideoLocation()
        response = self.uploadRequest(title, description, videoLocation)

    def uploadRequest(self, title, description, videoLocation):
        request = self.youtube.videos().insert(
            part="snippet,status",
            body={
            "snippet": {
                "categoryId": self.categoryId,
                "description": description,
                "title": title
            },
            "status": {
                "privacyStatus": "private"
            }
            },
            
            media_body=MediaFileUpload()
        )
        response = request.execute()
        print(response)
        return response
