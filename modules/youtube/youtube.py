from modules.youtube.google import Create_Service
from modules.youtube.uploader import YoutubeUploader


class YoutubeManager():
    def __init__(self, fileManager):
        self.client_secrets_file = "modules/youtube/client_secret.json"
        self.scopes = ["https://www.googleapis.com/auth/youtube.upload"]
        self.api_service_name = "youtube"
        self.api_version = "v3"

        self.youtube = self.auth()  
        self.fileManager = fileManager
        self.uploader = YoutubeUploader(self.youtube, self.fileManager)

    def auth(self):
        service = Create_Service(self.client_secrets_file, self.api_service_name, self.api_version, self.scopes)
        return service

    def upload(self):
        self.youtube.upload()
