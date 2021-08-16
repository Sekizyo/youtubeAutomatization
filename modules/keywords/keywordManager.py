import random

class KeywordManager():
    def __init__(self):
        self.topics = ['lofi','lo-fi','hip hop','hip-hop',' lofihop','lofi hiphop','lo-fi hip-hop','jazz','ambition','chill','chillout','chillhop','lofi jazz', 'chilledcow','lofi playlist','lounge music','relax music','relax and lounge music','music for studies','gaming beats','study beats','music for car','only best lofi','best lofi','best music','radio lofi','lofi 24/7','cafe music','music for games','sleep music','music for sleeping','morning music','hiphop lofi','best hiphop','take lounge','mrbunnymusic','wetvibes','vibes','relaxing','insomnia']
        self.categories = ['ambient', 'relaxing', 'piano', 'beats', 'calm', 'lofi']

    def getRandomTopic(self):
        return self.getRandom(self.topics)

    def getRandomTopicList(self, count=1):
        topics = []
        for i in range(count):
            topics.append(self.getRandomTopic())

        return topics

    def getRandomCategory(self):
        return self.getRandom(self.categories)

    def getRandom(self, list_):
        index = random.randint(0, len(list_)-1)
        return list_[index]