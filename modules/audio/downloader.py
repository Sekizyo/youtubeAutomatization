import requests
import random
from bs4 import BeautifulSoup
from modules.keywords.keywordManager import KeywordManager

class AudioDownloadManager():
    def __init__(self, fileManager):
        self.fileManager = fileManager
        self.keywordManager = KeywordManager()
        self.mainLink = 'https://www.chosic.com/free-music/'

    def getSongList(self):
        category = self.keywordManager.getRandomCategory()
        request = f'{self.mainLink}/{category}/'
        response = self.executeGetRequest(request)

        soup = BeautifulSoup(response.text, 'html.parser')

        container = soup.find(class_="content-area primary") #contener
        songBlock = container.find_all(class_='track-info track') # item block

        for block in songBlock:
            author = block.find(class_='artist-name').text
            title = block.find(class_='trackF-title-inside').text
            credlink = block.find(class_='download-button track-download').get("href")

            creds, downloadUrl = self.proceedIntoUrl(credlink)
            self.saveSongToDB(author, title, creds, downloadUrl)
            

    def saveSongToDB(self, author, title, creds, downloadUrl):
        author = self.formatString(author)
        filename = f'"{title}"'
        filename = filename.replace('\n', '')
        filename = filename.replace(' ', '-')
        title = self.formatTitle(title)
        creds = self.formatString(creds, doubleString=True, endlines=True)


        response = self.executeGetRequest(downloadUrl, True)
        if not self.fileManager.checkIfAudioExists(f"'{filename}'"):
            self.fileManager.createAudio(filename, title, author, creds)
            self.fileManager.createAudioFromResponse(filename, response)

    def proceedIntoUrl(self, url):
        response = self.executeGetRequest(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        creds = soup.find(class_='copy-span-rect').text
        dowloadUrl = soup.find(class_='download track-download').get("data-url")

        return creds, dowloadUrl
    
    def formatTitle(self, title):
        title = self.formatString(title).replace(' ', '-')
        return title

    def formatString(self, string, doubleString=True, endlines=False):
        string.strip()
        if not endlines: string = string.replace('\n', '')
        if doubleString:
            string = f'"{string}"'
        return string

    def executeGetRequest(self, link, stream=False):
        try:
            response = requests.get(link, stream=stream, headers={'User-Agent': 'Mozilla/5.0'})
            return response
        except:
            raise

    def run(self):
        if not self.fileManager.getAudioUnrendered():
            self.getSongList()

