from moviepy.editor import AudioFileClip, ImageClip


class RenderManager():
    def __init__(self, fileManager):
        self.fileManager = fileManager

    def render(self):
        video = self.fileManager.getVideoUnrendered()[0]
        if video:
            try:

                videoID = video[0]
                audioID = video[1]
                thumbnailID = video[2]

                audio = self.fileManager.getAudioByID(audioID)[0]
                thumbnail = self.fileManager.getThumbnailByID(thumbnailID)[0]

                videoPath = f'{self.fileManager.videoDir}/{video[3]}.mp4'
                audioPath = f'{self.fileManager.audioDir}/{audio[1]}.mp3'
                thumbnailPath = f'{self.fileManager.imageDir}/{thumbnail[1]}.jpg'

                audio = AudioFileClip(audioPath)
                clip = ImageClip(thumbnailPath).set_duration(audio.duration)
                clip = clip.set_audio(audio)
                clip.write_videofile(videoPath, fps=12)

                self.fileManager.updateVideoRenderStatusByID(videoID, True)

            except:
                raise
        else:
            return None
            
    def run(self):
        if self.fileManager.getVideoUnrendered():
            self.render()
        else:
            self.fileManager.createVideo()
