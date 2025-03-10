from unittest                                                        import TestCase
from osbot_utils.helpers.llms.builders.LLM_Request__Builder__Open_AI import LLM_Request__Builder__Open_AI
from osbot_utils.helpers.llms.platforms.open_ai.API__LLM__Open_AI    import API__LLM__Open_AI, ENV_NAME_OPEN_AI__API_KEY
from osbot_utils.type_safe.Type_Safe                                 import Type_Safe
from osbot_utils.utils.Env                                           import load_dotenv, get_env
from osbot_utils.utils.Objects                                       import obj, __


class test_API__LLM__Open_AI(TestCase):

    @classmethod
    def setUpClass(cls):
        load_dotenv()
        if not get_env(ENV_NAME_OPEN_AI__API_KEY):
            import pytest
            pytest.skip(f"{ENV_NAME_OPEN_AI__API_KEY} not set")

        cls.api_llm = API__LLM__Open_AI()

    def test_execute_simple(self):
        system_prompt = 'today is monday the 13 of December 2025, just reply with the exact answer'
        user_prompt   = "what is today's month?"
        payload       = { "model": "gpt-4o-mini",
                          "messages": [{"role": "system", "content": system_prompt} ,
                                       {"role": "user"  , "content": user_prompt} ] }

        model           = "gpt-4o-mini"

        with LLM_Request__Builder__Open_AI() as _:
            _.llm_request_data.model = model
            _.add_message__system(system_prompt)
            _.add_message__user  (user_prompt)
            payload_2       = _.build_request_payload()
        assert payload  == payload_2

        response       = self.api_llm.execute(payload).get('data')
        assert obj(response).choices[0].message.content == 'December'

    def test_execute_with_structured_output(self):
        class Current_Month(Type_Safe):
            month: str # this is the current month

        system_prompt   = 'today is monday the 13 of December 2025, just reply with the exact answer'
        user_prompt     = "what is this month?"
        model           = 'gpt-4o-mini'
        with LLM_Request__Builder__Open_AI() as _:
            _.llm_request_data.model = model
            _.add_message__system(system_prompt)
            _.add_message__user  (user_prompt)
            _.set_function_call(parameters=Current_Month, function_name="get_current_month")
            payload = _.build_request_payload()

        from osbot_utils.utils.Dev import pprint
        assert payload == { 'messages': [ { 'content': 'today is monday the 13 of December 2025, just reply with the exact answer',
                                            'role'   : 'system'                 },
                                          { 'content': 'what is this month?'    ,
                                            'role'   : 'user'                   }],
                            'model'          : 'gpt-4o-mini',
                            'response_format': { 'json_schema': { 'name'  : 'get_current_month',
                                                                  'schema': { 'additionalProperties': False,
                                                                              'properties'          : { 'month': { 'description': 'this '
                                                                                                                                    'is '
                                                                                                                                    'the '
                                                                                                                                    'current '
                                                                                                                                    'month',
                                                                                                                     'type': 'string'}},
                                                                                'required'          : ['month'] ,
                                                                                'type'              : 'object'  },
                                                                  'strict': True},
                                                   'type'     : 'json_schema'}}

        response_json  = self.api_llm.execute(payload).get('data')
        json_data      = response_json.get('choices')[0].get('message').get('content')
        current_month  = Current_Month.from_json(json_data)

        assert current_month.obj() == __(month='December')