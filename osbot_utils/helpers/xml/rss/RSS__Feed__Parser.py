from typing                                     import Dict, Any
from osbot_utils.type_safe.primitives.domains.identifiers.Guid                   import Guid
from osbot_utils.helpers.xml.rss.RSS__Channel   import RSS__Channel
from osbot_utils.helpers.xml.rss.RSS__Feed      import RSS__Feed
from osbot_utils.helpers.xml.rss.RSS__Image     import RSS__Image
from osbot_utils.helpers.xml.rss.RSS__Item      import RSS__Item


class RSS__Feed__Parser:

    def from_dict(self, data: Dict[str, Any]) -> RSS__Feed: # Convert a dictionary (from XML) into an RSS__Feed object
        if 'channel' not in data:
            raise ValueError("Invalid RSS feed: no channel element found")

        channel_data = data['channel']
        rss_items    = []
        items        = channel_data.get('item', [])                                 # get raw items data
        if type(items) is not list:                                                 # handle case when only one item is present
            items = [items]                                                         # by converting it to a list
        for item_data in items:                                                     # Process items

            title       = self.element_text(item_data.get('title'      ))
            link        = self.element_text(item_data.get('link'       ))
            description = self.element_text(item_data.get('description'))
            guid        = self.extract_guid(item_data.get('guid'       ))
            pubDate     = self.element_text(item_data.get('pubDate'    ))
            creator     = self.element_text(item_data.get('creator'    ))
            categories  = self.ensure_is_list(item_data.get('category'))
            rss_item = RSS__Item(title       = title                    ,
                                 link        = link                     ,
                                 description = description              ,
                                 guid        = guid                     ,
                                 pubDate     = pubDate                  ,
                                 creator     = creator                  ,
                                 categories  = categories               ,
                                 content     = item_data.get('content'      , {}),
                                 thumbnail   = item_data.get('thumbnail'    , {}))


            known_fields = {'title', 'link', 'description', 'guid', 'pubDate',          # Move non-standard elements to extensions
                          'creator', 'category', 'content', 'thumbnail'}
            rss_item.extensions = {k: v for k, v in item_data.items()
                                   if k not in known_fields}
            rss_items.append(rss_item)

        # Create channel
        link = self.element_text(channel_data.get('link'))
        channel = RSS__Channel( title            = channel_data.get('title'          , ''),
                                link             = link                                   ,
                                description      = channel_data.get('description'    , ''),
                                language         = channel_data.get('language'       , ''),
                                last_build_date  = channel_data.get('lastBuildDate'      ),
                                items            = rss_items                              ,
                                update_frequency = channel_data.get('updateFrequency', ''),
                                update_period    = channel_data.get('updatePeriod'   , ''))


        # Process channel image if present
        if 'image' in channel_data:
            img_data = channel_data['image']
            if img_data:
                channel.image = RSS__Image( url     = img_data.get('url'       , '' ),
                                            title   = img_data.get('title'     , '' ),
                                            link    = img_data.get('link'      , '' ),
                                            width   = int(img_data.get('width' , 0 )),
                                            height  = int(img_data.get('height', 0 )))

        known_channel_fields = {'title', 'link', 'description', 'language',         # Move non-standard channel elements to extensions
                               'lastBuildDate', 'image', 'item', 'updateFrequency', 'updatePeriod'}
        channel.extensions = {k: v for k, v in channel_data.items()
                            if k not in known_channel_fields}

        rss_feed = RSS__Feed(channel = channel)
        return rss_feed

    def extract_guid(self, target):
        return Guid(self.extract_text(target))

    def ensure_is_list(self, target):
        if type(target) is list:
            return target
        if type(target) is str:
            return [target]
        if target:
            return [f'{target}']
        return []

    def element_text(self, target):
        if isinstance(target, list):
            for item in target:
                value = self.extract_text(item)
                if value:
                    return value
        value = self.extract_text(target)
        return value or f'{target}'

    def extract_text(self, target):
        if not target:
            return ''
        if isinstance(target, str):
            return target
        if isinstance(target, dict):
            return target.get('#text', '')
        return ''