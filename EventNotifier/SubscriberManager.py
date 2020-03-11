'''
Created on 2019-03-20

@author: Vitalij Gotovskij (Lithuania)
'''

class SubscriberManager(object):
    def __init__(self, eventName):
        self.subscribers = []
        self.__eventName = eventName

    def notify(self, *args, **kwargs):
        for subscriber in self.subscribers:
            subscriber(*args, **kwargs)

    def getName(self):
        return self.__eventName
