from modules.fileManager import FileManager
from modules.youtube.youtube import YoutubeManager
from modules.soundcloud.downloader import DownloadManager


class Main():
    def __init__(self):
        self.running = True
        self.fileManager = FileManager()
        self.youtubeManager = YoutubeManager()
        self.downloadManager = DownloadManager()

    def download(self):
        self.downloadManager.download()
        
    def render(self):
        pass

    def upload(self):
        pass

    def run(self):
        while self.running:
            self.download()
            self.render()
            self.upload()
