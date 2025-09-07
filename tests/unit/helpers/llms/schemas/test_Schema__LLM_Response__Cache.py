from unittest                                                     import TestCase
from osbot_utils.helpers.llms.schemas.Schema__LLM_Request         import Schema__LLM_Request
from osbot_utils.helpers.llms.schemas.Schema__LLM_Response        import Schema__LLM_Response
from osbot_utils.helpers.llms.schemas.Schema__LLM_Response__Cache import Schema__LLM_Response__Cache
from osbot_utils.utils.Objects                                    import __

class test_Schema__LLM_Response__Cache(TestCase):

    def test_json_roundtrip(self):
        llm_response = Schema__LLM_Response()
        llm_request  = Schema__LLM_Request ()
        cache_entry  = Schema__LLM_Response__Cache(llm__response=llm_response, llm__request=llm_request)

        assert cache_entry.obj() == __(cache_id                  = cache_entry.cache_id,
                                       llm__payload              = __()                ,
                                       llm__response             = __( response_id    = llm_response.response_id,
                                                                      timestamp      = llm_response.timestamp,
                                                                      response_data  = __()),
                                       llm__request              = __( request_data   = __(function_call = None,
                                                                                          temperature   = None,
                                                                                          top_p         = None,
                                                                                          max_tokens    = None,
                                                                                          model         = '',
                                                                                          platform      = '',
                                                                                          provider      = '',
                                                                                          messages      = [])),
                                       request__duration        = 0.0                 ,
                                       request__hash            = None                ,
                                       timestamp                = cache_entry.timestamp)


        cache_entry_roundtrip = Schema__LLM_Response__Cache.from_json(cache_entry.json())
        assert cache_entry_roundtrip.json() == cache_entry.json()

        cache_entry_2 = { 'cache_id'         : '915b1417'        ,
                          'llm__request'     : { 'request_data': { 'function_call': None,
                                                                  'max_tokens': 100,
                                                                  'messages': [ { 'content': 'Test disk '
                                                                                             'retrieval',
                                                                                  'role': 'user'}],
                                                                  'model': 'test-model',
                                                                  'platform': 'test-platform',
                                                                  'provider': 'test-provider',
                                                                  'temperature': 0.7,
                                                                  'top_p': None}},
                          'llm__response'    : { 'response_data': {'content': 'This is a test response'},
                                                 'response_id': '7e744c72',
                                                 'timestamp': 1741607991904},
                          'llm__payload'     : {}            ,
                          'request__duration': 0.0           ,
                          'request__hash'    : '347a144f9d'  ,
                          'timestamp'        : 1741607991906 }

        assert Schema__LLM_Response__Cache.from_json(cache_entry_2).json() == cache_entry_2