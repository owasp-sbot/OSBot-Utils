from unittest import TestCase

from osbot_utils.helpers.pubsub.PubSub__Client import PubSub__Client


class test_PubSub__Client(TestCase):
    def setUp(self):
        self.client = PubSub__Client()