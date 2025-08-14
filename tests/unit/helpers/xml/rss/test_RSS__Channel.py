from unittest                                       import TestCase
from osbot_utils.type_safe.primitives.safe_str.identifiers.Guid                       import Guid
from osbot_utils.helpers.xml.rss.RSS__Channel       import RSS__Channel
from osbot_utils.helpers.xml.rss.RSS__Feed__Parser  import RSS__Feed__Parser
from osbot_utils.helpers.xml.rss.RSS__Image         import RSS__Image
from osbot_utils.helpers.xml.rss.RSS__Item          import RSS__Item


class test_RSS__Channel(TestCase):
    def setUp(self):
        self.title = "Test Channel"
        self.link = "https://test.com"
        self.description = "Test Description"
        self.language = "en"
        self.channel = RSS__Channel(title       = self.title      ,
                                    link        = self.link       ,
                                    description = self.description,
                                    language    = self.language   )

    def test_base_attributes(self):
        assert self.channel.title       == self.title
        assert self.channel.link        == self.link
        assert self.channel.description == self.description
        assert self.channel.language    == self.language
        assert self.channel.items       == []
        assert self.channel.extensions  == {}

    def test_with_image(self):
        image = RSS__Image(
            url="https://test.com/image.jpg",
            title="Test Image",
            link="https://test.com",
            width=100,
            height=100
        )
        self.channel.image = image
        assert self.channel.image == image
        assert self.channel.image.width == 100
        assert self.channel.image.height == 100

    def test_with_items(self):
        item = RSS__Item(title       = "Test Item",
                         link        = "https://test.com/item",
                         description = "Test Item Description",
                         guid        = Guid(RSS__Feed__Parser().element_text({'#text': 'https://test.com/item', 'isPermaLink': 'false'})),
                         pubDate     = "Thu, 26 Dec 2024 15:03:13 GMT",
                         creator     = "Test Author" )
        self.channel.items = [item]
        assert len(self.channel.items) == 1
        assert self.channel.items[0].title == "Test Item"

    def test_with_extensions(self):
        extensions = {
            'sy:updatePeriod': 'hourly',
            'sy:updateFrequency': '1'
        }
        self.channel.extensions = extensions
        assert self.channel.extensions == extensions