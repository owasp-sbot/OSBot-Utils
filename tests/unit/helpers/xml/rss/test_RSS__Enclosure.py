from unittest                                   import TestCase
from osbot_utils.helpers.xml.rss.RSS__Enclosure import RSS__Enclosure


class test_RSS__Enclosure(TestCase):
    def setUp(self):
        self.url = "https://test.com/file.mp3"
        self.type = "audio/mpeg"
        self.length = 12345678
        self.enclosure = RSS__Enclosure(
            url=self.url,
            type=self.type,
            length=self.length
        )

    def test_attributes(self):
        assert self.enclosure.url == self.url
        assert self.enclosure.type == self.type
        assert self.enclosure.length == self.length

    def test_defaults(self):
        enclosure = RSS__Enclosure(
            url="https://test.com/file.mp3",
            type="audio/mpeg"
        )
        assert enclosure.length == 0  # Type_Safe will initialize integers to 0