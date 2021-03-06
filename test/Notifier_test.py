import pytest
from unittest.mock import Mock

import sys
# insert at 1, 0 is the script path (or '' in REPL)
if not '../event-notifier' in sys.path:
    sys.path.insert(1, '../event-notifier')
from EventNotifier.Notifier import Notifier


@pytest.fixture(scope="class")  # scope="function" is default
def logger():
    import logging

    l = logging.getLogger("multiprocessing")
    h = logging.StreamHandler()
    f = logging.Formatter("%(asctime)s: %(message)s")
    h.setFormatter(f)
    l.addHandler(h)
    l.setLevel(logging.ERROR)
    yield l


@pytest.fixture(scope="class")  # scope="function" is default
def notifier(logger):
    return Notifier(["onCreate", "onOpen", "onModify", "onClose", "onDelete"], logger)


@pytest.fixture(scope="class")  # scope="function" is default
def emptyNotifier(logger):
    return Notifier([], logger)


@pytest.fixture(scope="class")  # scope="function" is default
def notifierWithoutLogger(logger):
    return Notifier(["onCreate", "onOpen", "onModify", "onDelete"])


class TestNotifier:
    def test_initialised_OK(self, notifier):
        assert 5 == len(notifier.get_registered_events())


    def test_initiallyEmpty_OK(self, emptyNotifier):
        assert 0 == len(emptyNotifier.get_registered_events())


    def test_initialisedWithoutLogger_OK(self, notifierWithoutLogger):
        assert 4 == len(notifierWithoutLogger.get_registered_events())


    def test_initialisedWithRepeatedEventNames_Raises(self, notifierWithoutLogger):
        with pytest.raises(KeyError):
            Notifier(["onCreate", "onOpen", "onModify", "onDelete", "onOpen"])


    def test_supportedEventsAccessible_OK(self, notifierWithoutLogger):
        notifier = Notifier(["onCreate", "onOpen", "onModify", "onDelete", "onForget"])
        assert ["onCreate", "onOpen", "onModify", "onDelete", "onForget"] == notifier.get_registered_events()


    def test_fireEvent_OK(self, notifierWithoutLogger):
        onOpenCallback = Mock()

        notifierWithoutLogger.subscribe("onOpen", onOpenCallback)

        onOpenCallback.assert_not_called()
        notifierWithoutLogger.raise_event("onOpen", 77)
        onOpenCallback.assert_called_once_with(77)


    def test_fireEventWithNoneAsEventName_Raises(self, notifierWithoutLogger):
        onOpenCallback = Mock()

        notifierWithoutLogger.subscribe("onOpen", onOpenCallback)

        onOpenCallback.assert_not_called()
        with pytest.raises(KeyError):
            notifierWithoutLogger.raise_event(None, "event info")
        onOpenCallback.assert_not_called()


    def test_fireEventWithNoneAsParameter_OK(self, notifierWithoutLogger):
        onOpenCallback = Mock()

        notifierWithoutLogger.subscribe("onOpen", onOpenCallback)

        onOpenCallback.assert_not_called()
        notifierWithoutLogger.raise_event("onOpen", None)
        onOpenCallback.assert_called_once_with(None)
        notifierWithoutLogger.raise_event("onOpen", None, None, None)
        onOpenCallback.assert_called_with(None, None, None)
        assert(2 == onOpenCallback.call_count)


    def test_fireEventOnlyCorrectIsFired_OK(self, notifierWithoutLogger):
        onOpenCallback = Mock()
        onDeleteCallback = Mock()

        notifierWithoutLogger.subscribe("onOpen", onOpenCallback)

        onOpenCallback.assert_not_called()
        onDeleteCallback.assert_not_called()

        notifierWithoutLogger.raise_event("onDelete", 258)
        notifierWithoutLogger.subscribe("onDelete", onDeleteCallback)

        onOpenCallback.assert_not_called()
        onDeleteCallback.assert_not_called()

        notifierWithoutLogger.raise_event("onOpen", 99)
        onOpenCallback.assert_called_once_with(99)
        onDeleteCallback.assert_not_called()

        notifierWithoutLogger.raise_event("onDelete", "string as event")
        onOpenCallback.assert_called_once_with(99)
        onDeleteCallback.assert_called_once_with("string as event")


    def test_removedSubscriberIsNotFired_OK(self, notifierWithoutLogger):
        onCreateCallback = Mock()
        onModifyCallback = Mock()

        notifierWithoutLogger.subscribe("onCreate", onCreateCallback)
        notifierWithoutLogger.subscribe("onModify", onModifyCallback)

        onCreateCallback.assert_not_called()
        onModifyCallback.assert_not_called()

        notifierWithoutLogger.raise_event("onCreate", "event: test_removedSubscriberIsNotFired_OK - onCreate")
        onCreateCallback.assert_called_once_with("event: test_removedSubscriberIsNotFired_OK - onCreate")
        onModifyCallback.assert_not_called()

        notifierWithoutLogger.remove_subscribers_by_event_name("onCreate")
        notifierWithoutLogger.raise_event("onCreate", "event: second time")

        onCreateCallback.assert_called_once_with("event: test_removedSubscriberIsNotFired_OK - onCreate")
        onModifyCallback.assert_not_called()

        notifierWithoutLogger.raise_event("onModify", "onModify is still working...")
        onCreateCallback.assert_called_once_with("event: test_removedSubscriberIsNotFired_OK - onCreate")
        onModifyCallback.assert_called_once_with("onModify is still working...")


    def test_allRemovedNotFiredToo_OK(self, notifierWithoutLogger):
        onOpenCallback = Mock()
        onDeleteCallback = Mock()

        notifierWithoutLogger.subscribe("onOpen", onOpenCallback)
        notifierWithoutLogger.subscribe("onDelete", onDeleteCallback)

        onOpenCallback.assert_not_called()
        onDeleteCallback.assert_not_called()

        notifierWithoutLogger.raise_event("onOpen", "event: test_removedSubscriberIsNotFired_OK - onOpen")
        onOpenCallback.assert_called_once_with("event: test_removedSubscriberIsNotFired_OK - onOpen")
        onDeleteCallback.assert_not_called()

        notifierWithoutLogger.remove_all_subscribers()

        notifierWithoutLogger.raise_event("onOpen", "event: second time")

        onOpenCallback.assert_called_once_with("event: test_removedSubscriberIsNotFired_OK - onOpen")
        onDeleteCallback.assert_not_called()


    def test_repeatedlyAddingSameSubscriber_OK(self, notifierWithoutLogger):
        onCreateCallback = Mock()
        notifierWithoutLogger.subscribe("onCreate", onCreateCallback)
        notifierWithoutLogger.subscribe("onCreate", onCreateCallback)
        notifierWithoutLogger.subscribe("onCreate", onCreateCallback)

        onCreateCallback.assert_not_called()

        notifierWithoutLogger.raise_event("onCreate", "event: onCreate 2222")
        onCreateCallback.assert_called_once_with("event: onCreate 2222")


    #TODO: refactor this test to use parmetrised annotation
    def test_anyTypeAsEvent_OK(self):
        class Box:
            def __init__(self, name):
                self.name = name

        a = Box("keyBoxA")
        b = Box("keyBoxB")
        c = Box("keyBoxB")  # intentionally named this way to look like b

        notifier = Notifier(["onCreate", 5, 22.58, "onDelete", a, b])
        onCreateCallback = Mock()
        on5Callback      = Mock()
        onFloatCallback  = Mock()
        onBoxACallback   = Mock()
        onBoxBCallback   = Mock()

        notifier.subscribe("onCreate", onCreateCallback)
        notifier.subscribe(5, on5Callback)
        notifier.subscribe(22.58, onFloatCallback)
        notifier.subscribe(a, onBoxACallback)
        notifier.subscribe(b, onBoxBCallback)

        onCreateCallback.assert_not_called()
        on5Callback.assert_not_called()
        onFloatCallback.assert_not_called()
        onBoxACallback.assert_not_called()
        onBoxBCallback.assert_not_called()

        notifier.raise_event("onCreate", "event: onCreate !!!!")
        onCreateCallback.assert_called_once_with("event: onCreate !!!!")
        on5Callback.assert_not_called()
        onFloatCallback.assert_not_called()
        onBoxACallback.assert_not_called()
        onBoxBCallback.assert_not_called()

        with pytest.raises(KeyError):
            notifier.raise_event(6, "event: !!!!! 6 !!!!")   # unknown event - KeyError raised
        onCreateCallback.assert_called_once_with("event: onCreate !!!!")
        on5Callback.assert_not_called()
        onFloatCallback.assert_not_called()
        onBoxACallback.assert_not_called()
        onBoxBCallback.assert_not_called()

        notifier.raise_event(5, "event: !!!!! 5 !!!!") # this one is registered - OK
        onCreateCallback.assert_called_once_with("event: onCreate !!!!")
        on5Callback.assert_called_once_with("event: !!!!! 5 !!!!")
        onFloatCallback.assert_not_called()
        onBoxACallback.assert_not_called()
        onBoxBCallback.assert_not_called()

        with pytest.raises(KeyError):
            notifier.raise_event(22.59, "event: !!!!! 22.59 !!!!")  # unknown event - KeyError raised
        onCreateCallback.assert_called_once_with("event: onCreate !!!!")
        on5Callback.assert_called_once_with("event: !!!!! 5 !!!!")
        onFloatCallback.assert_not_called()
        onBoxACallback.assert_not_called()
        onBoxBCallback.assert_not_called()

        notifier.raise_event(22.58, "event: !!!!! 22.58 !!!!")  # this one is registered - OK
        onCreateCallback.assert_called_once_with("event: onCreate !!!!")
        on5Callback.assert_called_once_with("event: !!!!! 5 !!!!")
        onFloatCallback.assert_called_once_with("event: !!!!! 22.58 !!!!")
        onBoxACallback.assert_not_called()
        onBoxBCallback.assert_not_called()

        with pytest.raises(KeyError):
            notifier.raise_event(c, "event: Box c with name like it is b")  # unknown event (object is known, name is the same, but object is still different) - KeyError raised
        onCreateCallback.assert_called_once_with("event: onCreate !!!!")
        on5Callback.assert_called_once_with("event: !!!!! 5 !!!!")
        onFloatCallback.assert_called_once_with("event: !!!!! 22.58 !!!!")
        onBoxACallback.assert_not_called()
        onBoxBCallback.assert_not_called()

        notifier.raise_event(b, "event: Box b")
        onCreateCallback.assert_called_once_with("event: onCreate !!!!")
        on5Callback.assert_called_once_with("event: !!!!! 5 !!!!")
        onFloatCallback.assert_called_once_with("event: !!!!! 22.58 !!!!")
        onBoxACallback.assert_not_called()
        onBoxBCallback.assert_called_once_with("event: Box b")


    def test_notifySubscribersWithMultipleParams_OK(self, notifier):
        onModifyCallback = Mock()

        notifier.subscribe("onModify", onModifyCallback)

        onModifyCallback.assert_not_called()

        notifier.raise_event("onModify", "some text", 25, 16.99, named1 ="named param value", named2 = 25)
        onModifyCallback.assert_called_once_with("some text", 25, 16.99, named1 = "named param value", named2 = 25)


    def test_subscribeToAll_OK(self, notifier):
        onAnyCallback = Mock()

        notifier.subscribe_to_all(onAnyCallback)

        onAnyCallback.assert_not_called()

        notifier.raise_event("onCreate", "event specific info here", event_type="onCreate")
        onAnyCallback.assert_called_once_with("event specific info here", event_type="onCreate")

        notifier.raise_event("onOpen", "event specific info22 here", event_type="onOpen")
        onAnyCallback.assert_called_with("event specific info22 here", event_type="onOpen")
        assert (2 == onAnyCallback.call_count)

        notifier.raise_event("onClose", "event specific info33 here", event_type="onClose")
        onAnyCallback.assert_called_with("event specific info33 here", event_type="onClose")
        assert (3 == onAnyCallback.call_count)


    def test_subscribeToAllIfWasAlreadyRegisteredToOne_OK(self, notifier):
        onAnyCallback = Mock()

        notifier.subscribe("onCreate", onAnyCallback)
        notifier.subscribe_to_all(onAnyCallback)

        onAnyCallback.assert_not_called()

        notifier.raise_event("onCreate", "event specific info here", event_type="onCreate")
        onAnyCallback.assert_called_once_with("event specific info here", event_type="onCreate")

        notifier.raise_event("onOpen", "event specific info22 here", event_type="onOpen")
        onAnyCallback.assert_called_with("event specific info22 here", event_type="onOpen")
        assert (2 == onAnyCallback.call_count)

