'''
Created on 2019-02-22

@author: Vitalij Gotovskij (Lithuania) 
'''

from .SubscriberManager import SubscriberManager
import threading
import logging


class Notifier(object):
    
    def __init__(self, eventNames, logger=None):
        self.__notifiers = {};
        self.lock = threading.Lock()
        if not logger == None:
            self.logger = logger
        else:
            self.logger = self.__setupLogger()
               
        for eventName in eventNames:
            self.logger.info(f"Registering event notifier: \"{eventName}\"")
            if(eventName in self.__notifiers):
                raise KeyError("Duplicating names in notifiers' list input")
            self.__notifiers[eventName] = SubscriberManager(eventName);


    def __setupLogger(self):
        l = logging.getLogger("Notifier_Native")
        h = logging.StreamHandler()
        f = logging.Formatter("%(asctime)s: %(message)s")
        h.setFormatter(f)
        l.addHandler(h)
        l.setLevel(logging.WARNING)
        return l


    def fireEvent(self, eventName, *args, **kwargs):
        self.lock.acquire()
        try:
            self.logger.info(f"Firing event {eventName} with following args: {[*args]} {{**kwargs}}")
            self.__notifiers[eventName].notify(*args, **kwargs)
        finally:
            self.lock.release() 
    
    
    def __removeSubscribersForNotifier(self, notifier):
        notifier.subscribers.clear()


    def removeSubscribersByEventName(self, eventName):
        self.lock.acquire()
        try:
            self.__notifiers[eventName].subscribers.clear()
        finally:
            self.lock.release() 


    def removeAllSubscribers(self):
        self.lock.acquire()
        try:
            for key, notifier in self.__notifiers.items():
                self.__removeSubscribersForNotifier(notifier)
        finally:
            self.lock.release()
        
    def subscribe(self, eventName, subscriber):
        self.lock.acquire()
        try:
            self.logger.info(f"Adding event subscriber for event {eventName}...")
            if(subscriber not in self.__notifiers[eventName].subscribers):
                self.__notifiers[eventName].subscribers.append(subscriber)
                self.logger.info(f"...OK")
            else:
                self.logger.warning("Subscriber you are trying to add was registered already")
        finally:
            self.lock.release()


    def subscribeToAll(self, subscriber):
        try:
            self.lock.acquire()
            for subscriberManager in self.__notifiers.values():
                self.logger.info(f"Adding event subscriber for event {subscriberManager.getName()}...")
                if(subscriber not in subscriberManager.subscribers):
                    subscriberManager.subscribers.append(subscriber)
                    self.logger.info(f"...OK")
                else:
                    self.logger.warning("Subscriber you are trying to add was registered already")
        finally:
            self.lock.release()

    def getSupportedEvents(self):
        return list(self.__notifiers.keys())