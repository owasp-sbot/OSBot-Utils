import pytest
from unittest                                                                       import TestCase
from osbot_utils.type_safe.primitives.domains.http.safe_str.Safe_Str__Http__User_Agent import Safe_Str__Http__User_Agent


class test_Safe_Str__Http__User_Agent(TestCase):

    def test__init__(self):                                                             # Test Safe_Str__Http__User_Agent initialization
        user_agent = Safe_Str__Http__User_Agent('curl/7.68.0')
        assert type(user_agent)       is Safe_Str__Http__User_Agent
        assert str(user_agent)        == 'curl/7.68.0'
        assert user_agent             == 'curl/7.68.0'

    def test__browser_user_agents(self):                                                # Test major browser user agent strings
        chrome = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        assert Safe_Str__Http__User_Agent(chrome              ) == chrome

        firefox = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0'
        assert Safe_Str__Http__User_Agent(firefox             ) == firefox

        safari = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15'
        assert Safe_Str__Http__User_Agent(safari              ) == safari

        edge = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0'
        assert Safe_Str__Http__User_Agent(edge                ) == edge

    def test__mobile_user_agents(self):                                                 # Test mobile device user agent strings
        iphone = 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1'
        assert Safe_Str__Http__User_Agent(iphone              ) == iphone

        android = 'Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36'
        assert Safe_Str__Http__User_Agent(android             ) == android

        ipad = 'Mozilla/5.0 (iPad; CPU OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1'
        assert Safe_Str__Http__User_Agent(ipad                ) == ipad

    def test__bot_crawler_user_agents(self):                                            # Test search engine bot user agent strings
        googlebot = 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
        assert Safe_Str__Http__User_Agent(googlebot           ) == googlebot

        bingbot = 'Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)'
        assert Safe_Str__Http__User_Agent(bingbot             ) == bingbot

        facebookbot = 'facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)'
        assert Safe_Str__Http__User_Agent(facebookbot         ) == facebookbot

        twitterbot = 'Twitterbot/1.0'
        assert Safe_Str__Http__User_Agent(twitterbot          ) == twitterbot

    def test__api_client_user_agents(self):                                             # Test HTTP client library user agent strings
        assert Safe_Str__Http__User_Agent('curl/7.68.0'       ) == 'curl/7.68.0'
        assert Safe_Str__Http__User_Agent('python-requests/2.28.1') == 'python-requests/2.28.1'
        assert Safe_Str__Http__User_Agent('PostmanRuntime/7.32.3') == 'PostmanRuntime/7.32.3'
        assert Safe_Str__Http__User_Agent('axios/0.27.2'      ) == 'axios/0.27.2'
        assert Safe_Str__Http__User_Agent('node-fetch/2.6.7'  ) == 'node-fetch/2.6.7'
        assert Safe_Str__Http__User_Agent('Go-http-client/1.1') == 'Go-http-client/1.1'
        assert Safe_Str__Http__User_Agent('Java/11.0.12'      ) == 'Java/11.0.12'

    def test__custom_application_user_agents(self):                                     # Test custom application user agent strings
        assert Safe_Str__Http__User_Agent('MyApp/1.0 (compatible; +https://example.com)') == 'MyApp/1.0 (compatible; +https://example.com)'
        assert Safe_Str__Http__User_Agent('CustomBot/2.0 (+https://bot.example.com/)') == 'CustomBot/2.0 (+https://bot.example.com/)'
        assert Safe_Str__Http__User_Agent('InternalService/3.5.1') == 'InternalService/3.5.1'

    def test__whitespace_handling(self):                                                # Test trim_whitespace = True
        assert Safe_Str__Http__User_Agent('  curl/7.68.0  '  ) == 'curl/7.68.0'
        assert Safe_Str__Http__User_Agent('MyApp/1.0  '      ) == 'MyApp/1.0'
        assert Safe_Str__Http__User_Agent('  Chrome/120.0.0.0') == 'Chrome/120.0.0.0'

    def test__numeric_conversion(self):                                                 # Test conversion from numeric types
        assert Safe_Str__Http__User_Agent(12345              ) == '12345'
        assert Safe_Str__Http__User_Agent(999                ) == '999'

    def test__control_characters(self):                                                 # Control characters get replaced
        assert Safe_Str__Http__User_Agent('curl/7.68.0\x00test') == 'curl/7.68.0_test'
        assert Safe_Str__Http__User_Agent('MyApp\x01/1.0'    ) == 'MyApp_/1.0'
        assert Safe_Str__Http__User_Agent('Bot\x1F/2.0'      ) == 'Bot_/2.0'

    def test__empty_values(self):                                                       # Test allow_empty = False enforcement

        assert Safe_Str__Http__User_Agent(None ) == ''
        assert Safe_Str__Http__User_Agent(''   ) == ''
        assert Safe_Str__Http__User_Agent('   ') == ''                                  # Spaces only (will be trimmed)


    def test__max_length(self):                                                         # Test TYPE_SAFE_STR__HTTP__USER_AGENT__MAX_LENGTH = 512
        valid_512   = 'a' * 512
        invalid_513 = 'a' * 513

        assert Safe_Str__Http__User_Agent(valid_512           ) == valid_512

        with pytest.raises(ValueError) as exc_info:
            Safe_Str__Http__User_Agent(invalid_513)
        assert "in Safe_Str__Http__User_Agent, value exceeds maximum length of 512" in str(exc_info.value)

    def test__special_characters(self):                                                 # Test various special characters allowed in user agents
        assert Safe_Str__Http__User_Agent('App/1.0 (X11; Linux x86_64)') == 'App/1.0 (X11; Linux x86_64)'
        assert Safe_Str__Http__User_Agent('Bot/2.0 (+https://bot.example.com/)') == 'Bot/2.0 (+https://bot.example.com/)'
        assert Safe_Str__Http__User_Agent('Client_v1.2.3'    ) == 'Client_v1.2.3'
        assert Safe_Str__Http__User_Agent('Service-Name/1.0' ) == 'Service-Name/1.0'
        assert Safe_Str__Http__User_Agent('App.Name/2.5'     ) == 'App.Name/2.5'

    def test__version_formats(self):                                                    # Test different version number formats
        assert Safe_Str__Http__User_Agent('App/1.0'          ) == 'App/1.0'
        assert Safe_Str__Http__User_Agent('App/1.2.3'        ) == 'App/1.2.3'
        assert Safe_Str__Http__User_Agent('App/1.2.3.4'      ) == 'App/1.2.3.4'
        assert Safe_Str__Http__User_Agent('App/1.0-beta'     ) == 'App/1.0-beta'
        assert Safe_Str__Http__User_Agent('App/1.0-rc.1'     ) == 'App/1.0-rc.1'

    def test__platform_information(self):                                               # Test platform/OS information in user agents
        windows = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
        assert Safe_Str__Http__User_Agent(windows             ) == windows

        mac = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'
        assert Safe_Str__Http__User_Agent(mac                 ) == mac

        linux = 'Mozilla/5.0 (X11; Linux x86_64)'
        assert Safe_Str__Http__User_Agent(linux               ) == linux

    def test__str_and_repr(self):                                                       # Test string representations
        user_agent = Safe_Str__Http__User_Agent('curl/7.68.0')

        assert str(user_agent)        == 'curl/7.68.0'
        assert f"{user_agent}"        == 'curl/7.68.0'
        assert f"User-Agent: {user_agent}" == 'User-Agent: curl/7.68.0'