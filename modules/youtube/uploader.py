from googleapiclient.http import MediaFileUpload

class youtubeUploader():
    def __init__(self, youtube):
        self.scopes = ["https://www.googleapis.com/auth/youtube.upload"]
        self.api_service_name = "youtube"
        self.api_version = "v3"
        self.client_secrets_file = "client_secret.json"

        self.youtube = self.auth()
        self.categoryId = 10 # Music
        self.videoLocationDefault = '../storage/readyForUpload/'

    def createTitle(self, songName, authorName):
        return f'{songName} - {authorName} - beats to relax/study to'

    def createDescription(self, creds):
        return f"Thank you for listening, I hope you will have a good time\nCredits:\n–––––––––––––––––––––––––––––– \n{creds}\n ––––––––––––––––––––––––––––––"

    def createVideoLocation(self, videoName):
        return f'{self.videoLocationDefault}{videoName}'

    def upload(self):
        title = self.generateTitle()
        description = self.generateDescription()
        videoLocation = self.createVideoLocation()
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
                "privacyStatus": "public"
            }
            },
            
            media_body=MediaFileUpload()
        )
        response = request.execute()
        print(response)
        return response
