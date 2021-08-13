import json
import random

import requests


class ImageDownloadManager():
    def __init__(self, fileManager):
        self.fileManager = fileManager
        self.client_secrets_file = 'modules/image/client_secret.json'
        self.accessKey = self.getClientSecret()
        self.topics = ['6sMVjTLSkeQ', 'rnSKDHwwYUk'] # Nature, Architecture

    def getClientSecret(self):
        with open(self.client_secrets_file, 'r') as json_file:
            data = json.load(json_file)
        
        return data['keys']['accessKey']

    def getRandomPhoto(self):
        response = self.executeApiRequest('/photos/random', self.getRandomTopic())
        jsonData = self.getJsonFromResponse(response)

        photoID = self.getIdFromJson(jsonData)
        photoCreds = self.getCredsFromJson(jsonData)
        photoLink = self.getPhotoLinkFromJson(jsonData)

        photo = self.executeGetRequest(photoLink, True)
        self.fileManager.createPhotoFromResponse(photoID, photo)

        self.fileManager.createThumbnail(f"'{photoID}'", f"'{photoCreds}'")

    def getMultipleRandomPhotos(self):
        response = self.executeApiRequest('/photos/random', topicID=self.getRandomTopic(), count=30)
        jsonData = self.getJsonFromResponse(response)
        for data in jsonData:

            photoID = self.getIdFromJson(data)
            photoCreds = self.getCredsFromJson(data)
            photoLink = self.getPhotoLinkFromJson(data)

            photo = self.executeGetRequest(photoLink, True)
            self.fileManager.createPhotoFromResponse(photoID, photo)

            self.fileManager.createThumbnail(f"'{photoID}'", f"'{photoCreds}'")

    def getRandomTopic(self):
        id_ = random.randint(0, len(self.topics)-1)
        return self.topics[id_]

    def getIdFromJson(self, jsonData):
        return jsonData['id']

    def getPhotoLinkFromJson(self, jsonData):
        return jsonData['urls']['regular']

    def getCredsFromJson(self, jsonData):
        return jsonData['user']['links']['html']

    def getJsonFromResponse(self, response):
        return response.json()

    def executeApiRequest(self, endpoint, topicID='', count=''):
        link = 'https://api.unsplash.com'
        
        token = f'/?client_id={self.accessKey}'
        if topicID:
            token += f'&topics={topicID}'
        
        if count:
            token += f'&count={count}'


        response = self.executeGetRequest(f'{link}{endpoint}{token}')
        return response

    def executeGetRequest(self, link, stream=False):
        try:
            response = requests.get(link, stream=stream)
            return response
        except:
            raise   

    def run(self):
        if not self.fileManager.getThumbnailUnrendered():
            self.getMultipleRandomPhotos()