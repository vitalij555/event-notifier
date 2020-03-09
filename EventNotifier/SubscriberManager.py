'''
Created on 2019-03-20

@author: Vitalij Gotovskij (Lithuania)
'''

class SubscriberManager(object):

    def __init__(self):
        self.subscribers = []
        
        
    def notify(self, *args, **kwargs):
        for subscriber in self.subscribers:
            subscriber(*args, **kwargs)
