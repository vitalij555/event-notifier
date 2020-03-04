import pytest
from unittest.mock import Mock

import sys
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, '../src')
from Notifier import Notifier


@pytest.fixture(scope="class")  # scope="function" is default
def logger():
    import logging
    import time
    import multiprocessing

    l = logging.getLogger("multiprocessing")
    h = logging.StreamHandler()
    f = logging.Formatter("%(asctime)s: %(message)s")
    h.setFormatter(f)
    l.addHandler(h)
    l.setLevel(logging.ERROR)
    yield l


@pytest.fixture(scope="class")  # scope="function" is default
def notifier(logger):
    return Notifier(["onCreate", "onOpen", "Modify", "onDelete"], logger)


@pytest.fixture(scope="class")  # scope="function" is default
def emptyNotifier(logger):
    return Notifier([], logger)


@pytest.fixture(scope="class")  # scope="function" is default
def notifierWithoutLogger(logger):
    return Notifier(["onCreate", "onOpen", "Modify", "onDelete"])


class TestNotifier:
    # def setUpClass():
    #     print("Wow called")
    #
    # def tearDownClass():
    #     print("Wow teardown called...")

    def test_initialised_OK(self, notifier):
        assert 4 == len(notifier.notifiers)
        assert not notifier.lock.locked()


    def test_initiallyEmpty_OK(self, emptyNotifier):
        assert 0 == len(emptyNotifier.notifiers)
        assert not emptyNotifier.lock.locked()


    def test_initialisedWithoutLogger_OK(self, notifierWithoutLogger):
        assert 4 == len(notifierWithoutLogger.notifiers)
        assert not notifierWithoutLogger.lock.locked()




