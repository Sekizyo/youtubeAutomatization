import os


class RenderManager():
    def __init__(self, fileManager):
        self.fileManager = fileManager

    def render(self):
        video = self.fileManager.getVideoUnrendered()
        if video:
            try:

                videoID = video[0][0]
                audioID = video[0][1]
                thumbnailID = video[0][2]

                audio = self.fileManager.getAudioByID(audioID)[0]
                thumbnail = self.fileManager.getThumbnailByID(thumbnailID)[0]

                audioPath = f'{self.fileManager.audioDir}/{audio[1]}'
                thumbnailPath = f'{self.fileManager.imageDir}/{thumbnail[1]}'
                videoPath = f'{self.fileManager.videoDir}/{video[0][3]}'

                os.system(f'bash modules/render/render {thumbnailPath}.jpg {audioPath}.mp3 {videoPath}.mp4')

                self.fileManager.updateVideoRenderStatusByID(videoID, True)

            except:
                raise
        else:
            return None
            
    def run(self):
        if not self.fileManager.getVideoUnrendered(): 
            self.fileManager.createVideo()
            
        self.render()