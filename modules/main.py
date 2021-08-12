from modules.storage.fileManager import FileManager
from modules.soundcloud.downloader import DownloadManager
from modules.render.renderManager import RenderManager
from modules.youtube.youtube import YoutubeManager


class Main():
    def __init__(self):
        self.running = True
        self.fileManager = FileManager()
        self.downloadManager = DownloadManager(self.fileManager)
        self.renderManager = RenderManager(self.fileManager)
        self.youtubeManager = YoutubeManager(self.fileManager)

    def download(self):
        self.downloadManager.run()
        
    def render(self):
        self.renderManager.run()
        
    def upload(self):
        self.youtubeManager.run()

    def run(self):
        # while self.running:
        #     self.download()
        self.render()
        # self.upload()
