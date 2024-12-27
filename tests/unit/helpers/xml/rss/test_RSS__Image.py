from unittest                                   import TestCase
from osbot_utils.helpers.xml.rss.RSS__Image     import RSS__Image


class test_RSS__Image(TestCase):
    def setUp(self):
        self.url = "https://test.com/image.jpg"
        self.title = "Test Image"
        self.link = "https://test.com"
        self.width = 100
        self.height = 100
        self.image = RSS__Image(
            url=self.url,
            title=self.title,
            link=self.link,
            width=self.width,
            height=self.height
        )

    def test_attributes(self):
        assert self.image.url == self.url
        assert self.image.title == self.title
        assert self.image.link == self.link
        assert self.image.width == self.width
        assert self.image.height == self.height

    def test_defaults(self):
        image = RSS__Image(
            url="https://test.com/image.jpg",
            title="Test Image",
            link="https://test.com"
        )
        assert image.width == 0   # Type_Safe will initialize integers to 0
        assert image.height == 0