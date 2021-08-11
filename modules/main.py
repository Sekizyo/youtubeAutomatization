from modules.storage.fileManager import FileManager
from modules.youtube.youtube import YoutubeManager
from modules.soundcloud.downloader import DownloadManager


class Main():
    def __init__(self):
        self.running = True
        self.fileManager = FileManager()
        self.youtubeManager = YoutubeManager(self.fileManager)
        self.downloadManager = DownloadManager(self.fileManager)

    def download(self):
        # self.downloadManager.download()
        pass
        
    def render(self):
        pass

    def upload(self):
        self.youtubeManager.upload()

    def run(self):
        # while self.running:
        #     self.download()
        self.render()
        # self.upload()
