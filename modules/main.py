from modules.storage.fileManager import FileManager
from modules.audio.downloader import AudioDownloadManager
from modules.image.downloader import ImageDownloadManager
from modules.render.renderManager import RenderManager
from modules.youtube.youtube import YoutubeManager


class Main():
    def __init__(self):
        self.running = True
        self.fileManager = FileManager()

        self.audioDownloadManager = AudioDownloadManager(self.fileManager)
        self.imageDownloadManager = ImageDownloadManager(self.fileManager)
        self.renderManager = RenderManager(self.fileManager)
        self.youtubeManager = YoutubeManager(self.fileManager)

    def download(self):
        self.audioDownloadManager.run()
        self.imageDownloadManager.run()
        
    def render(self):
        self.renderManager.run()
        
    def upload(self):
        self.youtubeManager.run()

    def run(self):
        while self.running:
            self.download()
            self.render()
            # self.upload()
