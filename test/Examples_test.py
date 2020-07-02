import pytest
from unittest.mock import Mock

import sys
# insert at 1, 0 is the script path (or '' in REPL)
if not '../../event-notifier' in sys.path:
    sys.path.insert(1, '../../event-notifier')
from EventNotifier.SubscriberManager import SubscriberManager



class TestExamples:
    def test_subscribe_to_all(self):
        from EventNotifier import Notifier
        class CallableFileWatchdog:
            def __init__(self, pathToWatch):
                self.pathToWatch = pathToWatch


            def __call__(self, *args, **kwargs):
                if len(args) > 0:
                    print \
                        (f"Event {args[0]} at path {self.pathToWatch} is called with following simple args: {[*args]} and with following keyword args: { {**kwargs} }")

        callable_watchog = CallableFileWatchdog("some\\path\\here")
        notifier = Notifier(["onCreate", "onOpen", "onModify", "onClose", "onDelete"])

        notifier.subscribe_to_all(callable_watchog)

        notifier.raise_event("onCreate", "onCreate", fileName="test_file.txt")
        notifier.raise_event("onOpen", "onOpen", openMode="w+", fileName="test_file.txt")


    def test_get_registered_events(self):
        from EventNotifier import Notifier
        notifier = Notifier(["onCreate", "onOpen", "onModify", "onClose", "onDelete"])
        print(notifier.get_registered_events())


    def test_remove_subscribers_by_event_name(self):
        from EventNotifier import Notifier
        class FileWatchDog():
            def onOpen(self, fileName, openMode):
                print(f"File {fileName} opened with {openMode} mode")

            def onClose(self, fileName):
                print(f"File {fileName} closed")


        def onOpenStandaloneMethod(fileName, openMode):
            print(f"StandaloneMethod: File {fileName} opened with {openMode} mode")

        watchDog = FileWatchDog()

        notifier = Notifier(["onCreate", "onOpen", "onModify", "onClose", "onDelete"])

        notifier.subscribe("onOpen", watchDog.onOpen)
        notifier.subscribe("onOpen", onOpenStandaloneMethod)
        notifier.subscribe("onClose", watchDog.onClose)

        print("\nAfter subscription:")
        notifier.raise_event("onOpen", openMode="w+", fileName="test_file.txt")
        notifier.raise_event("onClose", fileName="test_file.txt")

        notifier.remove_subscribers_by_event_name("onOpen")

        print("\nAfter removal of onOpen subscribers:")
        notifier.raise_event("onOpen", openMode="w+", fileName="test_file.txt")
        notifier.raise_event("onClose", fileName="test_file.txt")

        notifier.remove_subscribers_by_event_name("onClose")

        print("\nAfter removal of onClose subscribers:")
        notifier.raise_event("onOpen", openMode="w+", fileName="test_file.txt")
        notifier.raise_event("onClose", fileName="test_file.txt")



    def test_remove_all_subscribers(self):
        from EventNotifier import Notifier
        class FileWatchDog():
            def onOpen(self, fileName, openMode):
                print(f"File {fileName} opened with {openMode} mode")

            def onClose(self, fileName):
                print(f"File {fileName} closed")


        def onOpenStandaloneMethod(fileName, openMode):
            print(f"StandaloneMethod: File {fileName} opened with {openMode} mode")

        watchDog = FileWatchDog()

        notifier = Notifier(["onCreate", "onOpen", "onModify", "onClose", "onDelete"])

        notifier.subscribe("onOpen", watchDog.onOpen)
        notifier.subscribe("onOpen", onOpenStandaloneMethod)
        notifier.subscribe("onClose", watchDog.onClose)

        print("\nAfter subscription:")
        notifier.raise_event("onOpen", openMode="w+", fileName="test_file.txt")
        notifier.raise_event("onClose", fileName="test_file.txt")

        notifier.remove_all_subscribers()

        print("\nAfter removal of all subscribers:")
        notifier.raise_event("onOpen", openMode="w+", fileName="test_file.txt")
        notifier.raise_event("onClose", fileName="test_file.txt")