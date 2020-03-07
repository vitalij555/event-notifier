'''
Created on 2019-02-22

@author: Vitalij Gotovskij (Lithuania) 
'''

from SubscriberManager import SubscriberManager
import threading
import logging

class Notifier(object):
    
    def __init__(self, eventNames, logger=None):
        self.notifiers = {};
        self.lock = threading.Lock()
        if not logger == None:
            self.logger = logger
        else:
            self.logger = self.__setupLogger()
               
        for eventName in eventNames:
            self.logger.info(f"Registering event notifier: \"{eventName}\"")
            if(eventName in self.notifiers):
                raise KeyError("Duplicating names in notifiers' list input")
            self.notifiers[eventName] = SubscriberManager();


    def __setupLogger(self):
        l = logging.getLogger("Notifier_Native")
        h = logging.StreamHandler()
        f = logging.Formatter("%(asctime)s: %(message)s")
        h.setFormatter(f)
        l.addHandler(h)
        l.setLevel(logging.WARNING)
        return l


    def fireEvent(self, eventName, event):
        self.lock.acquire()
        try:
            self.logger.info(f"Firing event {eventName} : {event}")
            self.notifiers[eventName].notify(event)  
        finally:
            self.lock.release() 
    
    
    def __removeSubscribersForNotifier(self, notifier):
        notifier.subscribers.clear()


    def removeSubscribersByEventName(self, eventName):
        self.lock.acquire()
        try:
            self.notifiers[eventName].subscribers.clear()
        finally:
            self.lock.release() 


    def removeAllSubscribers(self):
        self.lock.acquire()
        try:
            for key, notifier in self.notifiers.items():
                self.__removeSubscribersForNotifier(notifier)
        finally:
            self.lock.release()
        
        
    def addEventSubscriber(self, eventName, subscriber):
        self.lock.acquire()
        try:
            self.logger.info(f"Adding event subscriber for event {eventName}...")    
            if(subscriber not in self.notifiers[eventName].subscribers):       
                self.notifiers[eventName].subscribers.append(subscriber)
                self.logger.info(f"...OK")
            else:
                self.logger.warning("Subscriber you are trying to add was registered already")
        finally:
            self.lock.release()
