import os


class RenderManager():
    def __init__(self, fileManager):
        self.fileManager = fileManager

    def render(self):
        video = self.fileManager.getVideoUnrendered()
        try:

            videoID = video[0]
            audioID = video[1]
            thumbnailID = video[2]

            audio = self.fileManager.getAudioByID(audioID)
            thumbnail = self.fileManager.getThumbnailByID(thumbnailID)

            audioPath = audio[4]
            thumbnailPath = thumbnail[3]

            videoPath = self.fileManager.updateVideoPath

            os.system(f'bash render {thumbnailPath} {audioPath} {videoPath}')

            self.fileManager.updateVideoRenderStatus(videoID)
        except:
            raise
        
    def run(self):
        if self.fileManager.getVideoUnrendered(): 
            self.render()