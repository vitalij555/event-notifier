'''
Created on 2019-02-22

@author: Vitalij Gotovskij (Lithuania) 
'''

from .SubscriberManager import SubscriberManager
import logging


class Notifier(object):

    def __init__(self, event_names: list, logger=None):
        self.__notifiers = {};
        if logger is not None:
            self.logger = logger
        else:
            self.logger = Notifier.__setup_logger()

        for eventName in event_names:
            self.logger.info("Registering event notifier: \"%s\"" % eventName)
            if eventName in self.__notifiers:
                raise KeyError("Duplicating names in notifiers' list input")
            self.__notifiers[eventName] = SubscriberManager(eventName)

    @staticmethod
    def __setup_logger():
        l = logging.getLogger("Notifier_Native")
        h = logging.StreamHandler()
        f = logging.Formatter("%(asctime)s: %(message)s")
        h.setFormatter(f)
        l.addHandler(h)
        l.setLevel(logging.WARNING)
        return l

    def raise_event(self, event_name, *args, **kwargs):
        self.logger.info("Firing event %s with following args: %s %s" % (event_name, [*args], {**kwargs}))
        self.__notifiers[event_name].notify(*args, **kwargs)

    @staticmethod
    def __remove_subscribers_for_notifier(notifier):
        notifier.subscribers.clear()

    def remove_subscribers_by_event_name(self, event_name):
        self.__notifiers[event_name].subscribers.clear()

    def remove_all_subscribers(self):
        for key, notifier in self.__notifiers.items():
            Notifier.__remove_subscribers_for_notifier(notifier)

    def subscribe(self, event_name, subscriber):
        self.logger.info("Adding event subscriber for event %s..." % event_name)
        if subscriber not in self.__notifiers[event_name].subscribers:
            self.__notifiers[event_name].subscribers.append(subscriber)
            self.logger.info(f"...OK")
        else:
            self.logger.warning("Subscriber you are trying to add has already been registered")

    def subscribe_to_all(self, subscriber):
        for subscriberManager in self.__notifiers.values():
            self.logger.info(f"Adding event subscriber for event %s..." % subscriberManager.getName())
            if subscriber not in subscriberManager.subscribers:
                subscriberManager.subscribers.append(subscriber)
                self.logger.info(f"...OK")
            else:
                self.logger.warning("Subscriber you are trying to add has already been registered")

    def get_registered_events(self) -> list:
        return list(self.__notifiers.keys())
