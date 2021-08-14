import datetime
import http.client
import os
import random
from datetime import time

import httplib2
from apiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload


class YoutubeUploader():
    def __init__(self, youtube, fileManager):
        self.youtube = youtube
        self.fileManager = fileManager

        self.categoryId = 10 # Music
        self.videoDir = '/media/joseph/HDD1/Py_projects/youtubeAutomatization/modules/storage/workInProgress'

        self.maxRetries = 10
        self.retriableStatusCodes = [500, 502, 503, 504]
        self.retriableExceptions = (httplib2.HttpLib2Error, IOError, http.client.NotConnected, http.client.IncompleteRead, http.client.ImproperConnectionState, http.client.CannotSendRequest, http.client.CannotSendHeader, http.client.ResponseNotReady, http.client.BadStatusLine)

    def upload(self):
        try:
            self.prepForUpload()
        except:
            raise

    def prepForUpload(self):
        request = self.createRequest()
        response = self.executeUploadRequest(request)
        return response
        
    def getUploadTime(self):
        format = "%d-%m-%Y"

        now = datetime.datetime.now()
        now_date = now.strftime("%d-%m-%Y")

        start_date = now.strptime(now_date, format)
        start_date = start_date + datetime.timedelta(minutes=10)

        start_date = start_date.isoformat() + "Z"
        return start_date

    def createRequest(self):
        videoTitle, videoCreds, videoPath = self.fileManager.getVideoReady()

        request_body = {
            'snippet': {
                'categoryID': self.categoryId,
                'title': self.getTitleTemplate(videoTitle),
                'description': self.getCredsTemplate(videoCreds),
            },
            'status': {
                'privacyStatus': 'private',
                'publishAt': self.getUploadTime(),
                'selfDeclaredMadeForKids': False, 
            },
            'notifySubscribers': False
        }

        insertRequest = self.youtube.videos().insert(
            part='snippet,status',
            body=request_body,
            media_body=MediaFileUpload(videoPath, chunksize=-1, resumable=True)
        )

        return insertRequest

    def getTitleTemplate(self, videoTile):
        return f"'{videoTile} - beats to relax/study to'"

    def getCredsTemplate(self, videoCreds):
        audioCreds, imageCreds = videoCreds.split(', ')
        return f"'Thank you for listening, I hope you will have a good time\nCredits:\n–––––––––––––––––––––––––––––– \nAudio:\n{audioCreds}\nImage:\n{imageCreds}\n ––––––––––––––––––––––––––––––'"

    def resumable_upload(self, insertRequest):
        response = None
        error = None
        retry = 0
        while response is None:
            try:
                print ("Uploading file...")
                status, response = insertRequest.next_chunk()
                if response is not None:
                    if 'id' in response:
                        print ("Video id '%s' was successfully uploaded." % response['id'])
                    else:
                        exit("The upload failed with an unexpected response: %s" % response)
            except HttpError as e:
                if e.resp.status in self.retriableStatusCodes:
                    error = "A retriable HTTP error %d occurred:\n%s" % (e.resp.status,
                                                                        e.content)
                else:
                    raise

            except self.retriableExceptions as e:
                error = "A retriable error occurred: %s" % e

                if error is not None:
                    print (error)
                    retry += 1
                if retry > self.maxRetries:
                    exit("No longer attempting to retry.")

                max_sleep = 2 ** retry
                sleep_seconds = random.random() * max_sleep
                print ("Sleeping %f seconds and then retrying..." % sleep_seconds)
                time.sleep(sleep_seconds)

    def executeUploadRequest(self, request):
        try:
            response = self.resumable_upload(request)
            return response
        except:
            raise