import pytest
from unittest.mock import Mock

import sys
# insert at 1, 0 is the script path (or '' in REPL)
if not '../EventNotifier' in sys.path:
    sys.path.insert(1, '../EventNotifier')
from SubscriberManager import SubscriberManager


@pytest.fixture(scope="class")  # scope="function" is default
def subscriber():
    return SubscriberManager()


class TestSubscriberManager:
    # def setUpClass():
    #     print("Wow called")
    #
    # def tearDownClass():
    #     print("Wow teardown called...")

    def test_initiallyEmpty(self, subscriber):
        assert 0 == len(subscriber.subscribers)


    def test_subscriberCalled_Ok(self, subscriber):
        subscriberCallback = Mock()

        subscriberCallback.assert_not_called()
        subscriber.subscribers.append(subscriberCallback)
        subscriber.notify(5)
        subscriberCallback.assert_called_once_with(5)
        subscriber.notify(7)
        subscriberCallback.assert_called_with(7)

