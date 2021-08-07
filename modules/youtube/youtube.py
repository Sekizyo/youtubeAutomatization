import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from module.youtube.uploader import youtubeUploader

class youtube():
    def __init__(self):
        self.youtube = self.auth()  
        self.uploader = youtubeUploader(self.youtube)

    def auth(self):
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        # Get credentials and create an API client
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(self.client_secrets_file, self.scopes)
        credentials = flow.run_console()
        youtube = googleapiclient.discovery.build(self.api_service_name, self.api_version, credentials=credentials)

        return youtube

def main():
    youtube = youtube()

if __name__ == "__main__":
    main()