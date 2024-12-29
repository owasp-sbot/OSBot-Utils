TEST_DATA__BASIC_FEED = '''
<rss version="2.0">
    <channel>
        <title>Test Feed</title>
        <link>https://test.com</link>
        <description>Test Description</description>
        <language>en</language>
        <lastBuildDate>Thu, 26 Dec 2024 15:03:13 GMT</lastBuildDate>
    </channel>
</rss>
'''

TEST_DATA__FEED_WITH_ITEMS = '''
<rss version="2.0">
    <channel>
        <title>Test Feed</title>
        <link>https://test.com</link>
        <description>Test Description</description>
        <language>en</language>
        <item>
            <title>Test Item 1</title>
            <link>https://test.com/item1</link>
            <description>Description 1</description>
            <guid isPermaLink="false">https://test.com/item1</guid>
            <pubDate>Thu, 26 Dec 2024 15:03:13 GMT</pubDate>
            <creator>Author 1</creator>
        </item>
        <item>
            <title>Test Item 2</title>
            <link>https://test.com/item2</link>
            <description>Description 2</description>
            <guid isPermaLink="false">https://test.com/item2</guid>
            <pubDate>Thu, 26 Dec 2024 16:03:13 GMT</pubDate>
            <creator>Author 2</creator>
        </item>
    </channel>
</rss>
'''

TEST_DATA__FEED_WITH_MEDIA = '''
<rss version="2.0" xmlns:media="http://search.yahoo.com/mrss/">
    <channel>
        <title>Test Feed</title>
        <link>https://test.com</link>
        <description>Test Description</description>
        <language>en</language>
        <item>
            <title>Test Item</title>
            <link>https://test.com/item</link>
            <description>Description</description>
            <guid isPermaLink="false">https://test.com/item</guid>
            <pubDate>Thu, 26 Dec 2024 15:03:13 GMT</pubDate>
            <media:thumbnail url="https://test.com/thumb.jpg"/>
            <media:content url="https://test.com/image.jpg" medium="image">
                <media:title type="html">Test Image</media:title>
            </media:content>
        </item>        
    </channel>
</rss>
'''

TEST_DATA__TECH_NEWS__FEED_XML = '''<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:sy="http://purl.org/rss/1.0/modules/syndication/">
    <channel>
        <title>Tech News Daily</title>
        <link>https://technewsdaily.example.com</link>
        <description>Latest Technology News</description>
        <language>en-us</language>
        <lastBuildDate>Thu, 05 Dec 2024 01:33:01 +0530</lastBuildDate>
        <sy:updatePeriod>hourly</sy:updatePeriod>
        <sy:updateFrequency>1</sy:updateFrequency>
        <item>
            <title>New AI Breakthrough</title>
            <description><![CDATA[Major advancement in artificial intelligence research]]></description>
            <link>https://technewsdaily.example.com/2024/12/ai-breakthrough.html</link>
            <guid>https://technewsdaily.example.com/2024/12/ai-breakthrough.html</guid>
            <pubDate>Wed, 04 Dec 2024 22:53:00 +0530</pubDate>
            <author>editor@technewsdaily.example.com</author>
            <enclosure url="https://example.com/ai-image.jpg" type="image/jpeg" length="12216320"/>
        </item>
    </channel>
</rss>'''

TEST_DATA__TECH_NEWS__FEED_XML_JSON = { 'channel': { 'description': 'Latest Technology News',
                                                     'extensions': {},
                                                     'image'     : None,
                                                     'items': [ { 'categories': [],
                                                                  'content': {},
                                                                  'creator': 'None',
                                                                  'description': 'Major advancement in artificial '
                                                                                 'intelligence research',
                                                                  'enclosure' : None,
                                                                  'extensions': { 'author': 'editor@technewsdaily.example.com',
                                                                                  'enclosure': { 'length': '12216320',
                                                                                                 'type': 'image/jpeg',
                                                                                                 'url': 'https://example.com/ai-image.jpg'}},
                                                                  'guid': '2e0985da-6a11-54be-b557-39402ba4a8ad',
                                                                  'link': 'https://technewsdaily.example.com/2024/12/ai-breakthrough.html',
                                                                  'pubDate': 'Wed, 04 Dec 2024 22:53:00 +0530',
                                                                  'thumbnail': {},
                                                                  'title': 'New AI Breakthrough'}],
                                                     'language'         : 'en-us',
                                                     'last_build_date'  : 'Thu, 05 Dec 2024 01:33:01 +0530',
                                                     'link'             : 'https://technewsdaily.example.com',
                                                     'title'            : 'Tech News Daily',
                                                     'update_frequency' : '1'              ,
                                                     'update_period'    : 'hourly'         },
                                        'extensions': {},
                                        'namespaces': {},
                                        'version': '2.0'}

TEST_DATA__CYBER_NEWS__FEED_XML = '''<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0"
    xmlns:content="http://purl.org/rss/1.0/modules/content/"
    xmlns:wfw="http://wellformedweb.org/CommentAPI/"
    xmlns:dc="http://purl.org/dc/elements/1.1/"
    xmlns:atom="http://www.w3.org/2005/Atom"
    xmlns:sy="http://purl.org/rss/1.0/modules/syndication/"
    xmlns:slash="http://purl.org/rss/1.0/modules/slash/">

<channel>
    <title>Cyber Security Today</title>
    <atom:link href="https://cybersectoday.example.com/feed/" rel="self" type="application/rss+xml" />
    <link>https://cybersectoday.example.com/</link>
    <description>Latest in Cybersecurity</description>
    <lastBuildDate>Mon, 23 Dec 2024 14:00:00 +0000</lastBuildDate>
    <language>en-US</language>
    <sy:updatePeriod>hourly</sy:updatePeriod>
    <sy:updateFrequency>1</sy:updateFrequency>
    <generator>News Generator v1.0</generator>

    <image>
        <url>https://cybersectoday.example.com/logo.png</url>
        <title>Cyber Security Today</title>
        <link>https://cybersectoday.example.com/</link>
        <width>32</width>
        <height>32</height>
    </image>

    <item>
        <title>Understanding Zero Trust Architecture</title>
        <link>https://cybersectoday.example.com/zero-trust/</link>
        <dc:creator><![CDATA[Alice Johnson]]></dc:creator>
        <pubDate>Mon, 23 Dec 2024 13:00:00 +0000</pubDate>
        <category><![CDATA[Network Security]]></category>
        <category><![CDATA[Zero Trust]]></category>
        <guid isPermaLink="false">https://cybersectoday.example.com/zero-trust-article</guid>
        <description><![CDATA[<p>A comprehensive guide to implementing Zero Trust Architecture.</p>]]></description>
    </item>
</channel>
</rss>'''

TEST_DATA__CYBER_NEWS__FEED_XML__JSON = {'channel': {'description': 'Latest in Cybersecurity',
                                                     'extensions': {'generator': 'News Generator v1.0'},
                                                     'image': {'height'      : 32,
                                                               'link'        : 'https://cybersectoday.example.com/',
                                                               'title'       : 'Cyber Security Today',
                                                               'url'         : 'https://cybersectoday.example.com/logo.png',
                                                               'width'       : 32},
                                                     'items': [{'categories' : ['Network Security', 'Zero Trust'],
                                                                'content'    : {},
                                                                'creator'    : 'Alice Johnson',
                                                                'description': '<p>A comprehensive guide to '
                                                                               'implementing Zero Trust '
                                                                               'Architecture.</p>',
                                                                'enclosure'  : None,
                                                                'extensions' : {},
                                                                'guid'       : '3bcf5c44-9fb7-58eb-97ea-952d101c0eac',
                                                                'link'       : 'https://cybersectoday.example.com/zero-trust/',
                                                                'pubDate'    : 'Mon, 23 Dec 2024 13:00:00 +0000',
                                                                'thumbnail'  : {},
                                                                'title': 'Understanding Zero Trust Architecture'}],
                                                     'language': 'en-US',
                                                     'last_build_date': 'Mon, 23 Dec 2024 14:00:00 +0000',
                                                     'link': 'https://cybersectoday.example.com/',
                                                     'title': 'Cyber Security Today',
                                                     'update_frequency': '1',
                                                     'update_period'   : 'hourly'},
                                         'extensions': {},
                                         'namespaces': {},
                                         'version': '2.0'}

TEST_DATA__SECURITY_ALERTS__FEED_XML = '''<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" 
    xmlns:dc="http://purl.org/dc/elements/1.1/" 
    xmlns:atom="http://www.w3.org/2005/Atom" 
    xmlns:media="http://search.yahoo.com/mrss/">
<channel>
    <title>Security Alerts Daily</title>
    <link>https://secalerts.example.com</link>
    <description>Security Alert Feed</description>
    <language>en</language>
    <atom:link href="https://secalerts.example.com/feeds/rss.xml" rel="self" type="application/rss+xml"/>
    <item>
        <title>Critical Vulnerability Alert</title>
        <link>https://secalerts.example.com/vuln/critical-update</link>
        <description>High-severity vulnerability discovered in popular software</description>
        <pubDate>Thu, 26 Dec 2024 15:03:13 GMT</pubDate>
        <dc:creator>Security Research Team</dc:creator>
        <guid isPermaLink="false">https://secalerts.example.com/vuln/critical-update</guid>
        <media:thumbnail url="https://secalerts.example.com/images/alert.jpg"/>
        <media:content url="https://secalerts.example.com/images/alert-full.jpg" medium="image">
            <media:title type="html">Vulnerability Analysis</media:title>
        </media:content>
    </item>
</channel>
</rss>'''

TEST_DATA__SECURITY_ALERTS__FEED_XML__JSON = {'channel': {'description': 'Security Alert Feed',
                                                          'extensions': {},
                                                          'image': None,
                                                          'items': [{'categories': [],
                                                                     'content': {'medium': 'image',
                                                                                 'title': {'#text': 'Vulnerability Analysis',
                                                                                           'type': 'html'},
                                                                                 'url': 'https://secalerts.example.com/images/alert-full.jpg'},
                                                                     'creator': 'Security Research Team',
                                                                     'description': 'High-severity vulnerability discovered '
                                                                                    'in popular software',
                                                                     'enclosure': None,
                                                                     'extensions': {},
                                                                     'guid': '31f9ab91-c1c4-5051-89a3-3f3f9acd68dd',
                                                                     'link': 'https://secalerts.example.com/vuln/critical-update',
                                                                     'pubDate': 'Thu, 26 Dec 2024 15:03:13 GMT',
                                                                     'thumbnail': {'url': 'https://secalerts.example.com/images/alert.jpg'},
                                                                     'title': 'Critical Vulnerability Alert'}],
                                                          'language': 'en',
                                                          'last_build_date': '',
                                                          'link': 'https://secalerts.example.com',
                                                          'title': 'Security Alerts Daily',
                                                          'update_frequency': '',
                                                           'update_period': '',},
                                              'extensions': {},
                                              'namespaces': {},
                                              'version': '2.0'}

TEST_DATA__RSS_FEED__MULTIPLE_ITEMS = {   "version": "2.0",
                                          "channel": {
                                            "image": None,
                                            "description": "Trusted independent cybersecurity news source for everyone.",
                                            "extensions": {},
                                            "items": [
                                              {
                                                "title": "Critical Vulnerability in Popular Network Routers Exposes Thousands to Exploits",
                                                "link": "https://example.com/critical-router-exploit",
                                                "description": "A new high-severity flaw has been discovered in widely used routers, allowing remote attackers to execute arbitrary commands.",
                                                "guid": "1a2b3c4d-5678-90ef-1234-567890abcdef",
                                                "pubDate": "Sat, 28 Dec 2024 11:55:00 +0530",
                                                "creator": "None"
                                              },
                                              {
                                                "title": "Hackers Deploy Malware via Fake Job Offers in Social Engineering Campaign",
                                                "link": "https://example.com/malware-fake-job-offers",
                                                "description": "Cybercriminals are using fake job offers to distribute new malware variants, tricking victims into compromising their own systems.",
                                                "guid": "2b3c4d5e-6789-01fg-2345-678901bcdefg",
                                                "pubDate": "Fri, 27 Dec 2024 23:12:00 +0530",
                                                "creator": "None"
                                              },
                                              {
                                                "title": "Security Flaw in Enterprise Software Could Lead to Data Breaches",
                                                "link": "https://example.com/software-security-flaw",
                                                "description": "An identified vulnerability in popular enterprise software could expose sensitive data if left unpatched.",
                                                "guid": "3c4d5e6f-7890-12gh-3456-789012cdefgh",
                                                "pubDate": "Fri, 27 Dec 2024 16:40:00 +0530",
                                                "creator": "None"
                                              },
                                              {
                                                "title": "New AI Techniques Help Cybercriminals Generate Undetectable Malware",
                                                "link": "https://example.com/ai-undetectable-malware",
                                                "description": "Cybersecurity researchers warn that AI is being used to create advanced malware capable of bypassing traditional detection methods.",
                                                "guid": "4d5e6f7g-8901-23ij-4567-890123defghi",
                                                "pubDate": "Mon, 23 Dec 2024 19:18:00 +0530",
                                                "creator": "None"
                                              }
                                            ],
                                            "language": "en-us",
                                            "last_build_date": "Sun, 29 Dec 2024 16:13:23 +0530",
                                            "link": "https://example.com",
                                            "title": "Cybersecurity News",
                                            "update_frequency": "1",
                                            "update_period": "hourly"
                                          },
                                          "namespaces": {},
                                          "extensions": {}
                                        }